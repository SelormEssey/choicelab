import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app
from study.fixtures import TRIALS, fixture_checksum
from study.models import STUDY_VERSION, Condition, SessionStatus
from study.routes import get_service
from study.service import StudyService


@pytest.fixture()
def service(tmp_path: Path) -> StudyService:
    instance = StudyService(tmp_path / "study.sqlite3")
    instance._choose_condition_and_schedule = lambda connection: (Condition.AI_RECOMMENDATION, "A")  # type: ignore[method-assign]
    return instance


@pytest.fixture()
def client(service: StudyService) -> TestClient:
    app.dependency_overrides[get_service] = lambda: service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def create_session(client: TestClient) -> str:
    response = client.post("/v1/study/sessions", json={"consent": True})
    assert response.status_code == 201
    return response.json()["session_id"]


def respond_to_current_trial(client: TestClient, session_id: str, selected: str | None = None) -> dict:
    trial = client.get(f"/v1/study/sessions/{session_id}/current-trial").json()
    attempt = client.post(
        f"/v1/study/sessions/{session_id}/trial-attempts", json={"trial_id": trial["id"]}
    ).json()
    response = client.post(
        f"/v1/study/sessions/{session_id}/responses",
        json={
            "trial_id": trial["id"],
            "attempt_id": attempt["attempt_id"],
            "selected_option_id": selected or trial["options"][0]["id"],
            "participant_confidence": 50,
            "response_time_ms": 1200,
            "idempotency_key": f"retry-key-{trial['id']}-0001",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_existing_endpoints(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/v1/project-status").status_code == 200


def test_consent_and_client_condition_are_required(client: TestClient) -> None:
    assert client.post("/v1/study/sessions", json={"consent": False}).status_code == 422
    assert (
        client.post("/v1/study/sessions", json={"consent": True, "condition": "CONTROL"}).status_code == 422
    )
    session_id = create_session(client)
    session = client.get(f"/v1/study/sessions/{session_id}").json()
    assert session["study_version"] == STUDY_VERSION
    assert session["status"] == SessionStatus.IN_PROGRESS


def test_fixtures_are_versioned_valid_and_balanced() -> None:
    assert len(TRIALS) == 10
    assert fixture_checksum()
    for trial in TRIALS:
        options = {option.id for option in trial.options}
        assert trial.correct_option_id in options
        assert trial.incorrect_ai_option_id in options - {trial.correct_option_id}


def test_assigned_schedule_persists_balanced_stimuli_and_option_order(
    client: TestClient, service: StudyService
) -> None:
    session_id = create_session(client)
    with service._connection() as connection:
        rows = connection.execute(
            "SELECT option_order_json, stimulus_json FROM session_trials WHERE session_id = ?", (session_id,)
        ).fetchall()
    assert len(rows) == 10
    assert sum(json.loads(row["stimulus_json"])["recommendation_correct"] for row in rows) == 5
    assert all(len(json.loads(row["option_order_json"])) in {2, 3} for row in rows)


def test_current_trial_redacts_scoring_and_persists_attempt(client: TestClient) -> None:
    session_id = create_session(client)
    trial = client.get(f"/v1/study/sessions/{session_id}/current-trial").json()
    assert "correct_option_id" not in trial
    assert "recommendation_correct" not in trial
    attempt = client.post(f"/v1/study/sessions/{session_id}/trial-attempts", json={"trial_id": trial["id"]})
    assert attempt.status_code == 201
    assert attempt.json()["attempt_number"] == 1


def test_server_computes_response_and_prevents_duplicate(client: TestClient, service: StudyService) -> None:
    session_id = create_session(client)
    trial = client.get(f"/v1/study/sessions/{session_id}/current-trial").json()
    attempt = client.post(
        f"/v1/study/sessions/{session_id}/trial-attempts", json={"trial_id": trial["id"]}
    ).json()
    payload = {
        "trial_id": trial["id"],
        "attempt_id": attempt["attempt_id"],
        "selected_option_id": trial["assistance"]["recommendation_option_id"],
        "participant_confidence": 80,
        "response_time_ms": 1500,
        "idempotency_key": "same-key-for-retry-001",
    }
    assert (
        client.post(
            f"/v1/study/sessions/{session_id}/responses", json={**payload, "selected_correct_option": True}
        ).status_code
        == 422
    )
    assert client.post(f"/v1/study/sessions/{session_id}/responses", json=payload).status_code == 200
    assert client.post(f"/v1/study/sessions/{session_id}/responses", json=payload).status_code == 200
    with service._connection() as connection:
        saved = connection.execute(
            "SELECT followed_ai, selected_correct_option FROM trial_responses WHERE session_id = ?",
            (session_id,),
        ).fetchone()
    assert saved["followed_ai"] == 1
    assert saved["selected_correct_option"] in {0, 1}


def test_invalid_option_confidence_and_stale_trial_are_rejected(client: TestClient) -> None:
    session_id = create_session(client)
    trial = client.get(f"/v1/study/sessions/{session_id}/current-trial").json()
    attempt = client.post(
        f"/v1/study/sessions/{session_id}/trial-attempts", json={"trial_id": trial["id"]}
    ).json()
    payload = {
        "trial_id": trial["id"],
        "attempt_id": attempt["attempt_id"],
        "selected_option_id": "not-an-option",
        "participant_confidence": 101,
        "response_time_ms": 50,
        "idempotency_key": "validation-failure-0001",
    }
    assert client.post(f"/v1/study/sessions/{session_id}/responses", json=payload).status_code == 422
    assert (
        client.post(
            f"/v1/study/sessions/{session_id}/trial-attempts", json={"trial_id": "future-trial"}
        ).status_code
        == 409
    )


def test_control_never_receives_or_records_ai_following(service: StudyService) -> None:
    service._choose_condition_and_schedule = lambda connection: (Condition.CONTROL, "A")  # type: ignore[method-assign]
    app.dependency_overrides[get_service] = lambda: service
    with TestClient(app) as client:
        session_id = create_session(client)
        trial = client.get(f"/v1/study/sessions/{session_id}/current-trial").json()
        assert trial["assistance"] is None
        respond_to_current_trial(client, session_id)
    app.dependency_overrides.clear()
    with service._connection() as connection:
        response = connection.execute(
            "SELECT followed_ai, ai_recommendation_correct FROM trial_responses WHERE session_id = ?",
            (session_id,),
        ).fetchone()
    assert response["followed_ai"] is None
    assert response["ai_recommendation_correct"] is None


def test_questionnaire_is_gated_and_debrief_is_terminal(client: TestClient) -> None:
    session_id = create_session(client)
    assert client.get(f"/v1/study/sessions/{session_id}/questionnaire").status_code == 409
    assert client.get(f"/v1/study/sessions/{session_id}/debrief").status_code == 409
    assert client.post(f"/v1/study/sessions/{session_id}/stop").status_code == 204
    assert client.get(f"/v1/study/sessions/{session_id}/debrief").status_code == 200
    assert client.get(f"/v1/study/sessions/{session_id}/current-trial").status_code == 409


def test_completed_session_questionnaire_and_persistence(client: TestClient, service: StudyService) -> None:
    session_id = create_session(client)
    for _ in range(10):
        respond_to_current_trial(client, session_id)
    questionnaire = client.get(f"/v1/study/sessions/{session_id}/questionnaire").json()
    responses = {item["id"]: 3 for item in questionnaire["items"]}
    assert (
        client.post(f"/v1/study/sessions/{session_id}/post-study", json={"responses": responses}).status_code
        == 204
    )
    assert client.get(f"/v1/study/sessions/{session_id}").json()["status"] == SessionStatus.COMPLETED
    reopened = StudyService(service.database_path)
    assert reopened.progress(session_id).status == SessionStatus.COMPLETED


def test_questionnaire_requires_exact_applicable_items(client: TestClient) -> None:
    session_id = create_session(client)
    for _ in range(10):
        respond_to_current_trial(client, session_id)
    assert (
        client.post(f"/v1/study/sessions/{session_id}/post-study", json={"responses": {}}).status_code == 422
    )
