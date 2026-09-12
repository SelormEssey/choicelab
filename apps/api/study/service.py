from __future__ import annotations

import json
import secrets
import sqlite3
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from fastapi import HTTPException, status

from .database import connect, initialize
from .fixtures import TRIALS, fixture_checksum, trial_by_id
from .models import CONSENT_VERSION, STUDY_VERSION, Condition, SessionStatus
from .questionnaire import SCALE, items_for
from .schemas import (
    AssistanceView,
    DebriefView,
    OptionView,
    QuestionnaireRequest,
    QuestionnaireView,
    ResearcherSummary,
    SessionCreated,
    SessionProgress,
    TrialAttemptCreated,
    TrialResponseReceipt,
    TrialResponseRequest,
    TrialView,
)


def now() -> str:
    return datetime.now(UTC).isoformat()


def fail(code: int, detail: str) -> HTTPException:
    return HTTPException(status_code=code, detail=detail)


class StudyService:
    """Study rules and persistence boundary. SQLite can be replaced behind this API."""

    def __init__(self, database_path: Path | None = None) -> None:
        self.database_path = database_path
        initialize(database_path)

    def _connection(self) -> sqlite3.Connection:
        return connect(self.database_path)

    def _session(self, connection: sqlite3.Connection, session_id: str) -> sqlite3.Row:
        row = connection.execute("SELECT * FROM study_sessions WHERE id = ?", (session_id,)).fetchone()
        if row is None:
            raise fail(status.HTTP_404_NOT_FOUND, "Study session was not found.")
        return row

    def authorize(self, session_id: str, token: str | None) -> None:
        if not token:
            raise fail(status.HTTP_401_UNAUTHORIZED, "A session token is required.")
        with self._connection() as connection:
            session = self._session(connection, session_id)
            expected = session["access_token_hash"]
            supplied = sha256(token.encode("utf-8")).hexdigest()
            if not expected or not secrets.compare_digest(expected, supplied):
                raise fail(status.HTTP_403_FORBIDDEN, "The session token is invalid.")

    def _choose_condition_and_schedule(self, connection: sqlite3.Connection) -> tuple[Condition, str]:
        condition_rows = connection.execute(
            "SELECT condition, COUNT(*) AS count FROM study_sessions WHERE study_version = ? GROUP BY condition",
            (STUDY_VERSION,),
        ).fetchall()
        counts = {condition: 0 for condition in Condition}
        counts.update({Condition(row["condition"]): row["count"] for row in condition_rows})
        least = min(counts.values())
        candidates = [condition for condition in Condition if counts[condition] == least]
        condition = secrets.choice(candidates)
        schedule_rows = connection.execute(
            "SELECT schedule_id, COUNT(*) AS count FROM study_sessions WHERE study_version = ? AND condition = ? GROUP BY schedule_id",
            (STUDY_VERSION, condition.value),
        ).fetchall()
        schedule_counts = {"A": 0, "B": 0}
        schedule_counts.update({row["schedule_id"]: row["count"] for row in schedule_rows})
        least_schedule = min(schedule_counts.values())
        schedule = secrets.choice([key for key, value in schedule_counts.items() if value == least_schedule])
        return condition, schedule

    def create_session(self) -> SessionCreated:
        session_id = f"ses_{secrets.token_urlsafe(18)}"
        session_token = secrets.token_urlsafe(32)
        access_token_hash = sha256(session_token.encode("utf-8")).hexdigest()
        participant_id = f"P-{secrets.token_hex(4).upper()}"
        timestamp = now()
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            condition, schedule = self._choose_condition_and_schedule(connection)
            connection.execute(
                """INSERT INTO study_sessions
                (id, access_token_hash, anonymous_participant_id, condition, schedule_id, status, study_version,
                 fixture_checksum, consent_version, consented_at, started_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    session_id,
                    access_token_hash,
                    participant_id,
                    condition.value,
                    schedule,
                    SessionStatus.IN_PROGRESS.value,
                    STUDY_VERSION,
                    fixture_checksum(),
                    CONSENT_VERSION,
                    timestamp,
                    timestamp,
                ),
            )
            trial_ids = [trial.id for trial in TRIALS]
            secrets.SystemRandom().shuffle(trial_ids)
            for order, trial_id in enumerate(trial_ids):
                trial = trial_by_id(trial_id)
                option_ids = [entry.id for entry in trial.options]
                secrets.SystemRandom().shuffle(option_ids)
                correct_advice = (order % 2 == 0) if schedule == "A" else (order % 2 != 0)
                recommendation = trial.correct_option_id if correct_advice else trial.incorrect_ai_option_id
                stimulus = {
                    "recommendation_option_id": recommendation,
                    "recommendation_correct": correct_advice,
                    "explanation": trial.explanation_correct
                    if correct_advice
                    else trial.explanation_incorrect,
                    "confidence_percent": trial.confidence_correct
                    if correct_advice
                    else trial.confidence_incorrect,
                }
                connection.execute(
                    "INSERT INTO session_trials(session_id, trial_id, trial_order, option_order_json, stimulus_json) VALUES (?, ?, ?, ?, ?)",
                    (session_id, trial_id, order, json.dumps(option_ids), json.dumps(stimulus)),
                )
            connection.commit()
        return SessionCreated(
            session_id=session_id,
            session_token=session_token,
            anonymous_participant_id=participant_id,
            status=SessionStatus.IN_PROGRESS,
            study_version=STUDY_VERSION,
        )

    def progress(self, session_id: str) -> SessionProgress:
        with self._connection() as connection:
            session = self._session(connection, session_id)
            return SessionProgress(
                session_id=session["id"],
                status=SessionStatus(session["status"]),
                current_trial_index=session["current_trial_index"],
                total_trials=len(TRIALS),
                study_version=session["study_version"],
                started_at=datetime.fromisoformat(session["started_at"]),
                completed_at=datetime.fromisoformat(session["completed_at"])
                if session["completed_at"]
                else None,
            )

    def current_trial(self, session_id: str) -> TrialView:
        with self._connection() as connection:
            session = self._session(connection, session_id)
            if session["status"] != SessionStatus.IN_PROGRESS.value:
                raise fail(status.HTTP_409_CONFLICT, "This session does not have an active trial.")
            stored = connection.execute(
                "SELECT * FROM session_trials WHERE session_id = ? AND trial_order = ?",
                (session_id, session["current_trial_index"]),
            ).fetchone()
            if stored is None:
                raise fail(status.HTTP_409_CONFLICT, "No current trial is available.")
            trial = trial_by_id(stored["trial_id"])
            option_map = {entry.id: entry for entry in trial.options}
            ordered_options = [option_map[id] for id in json.loads(stored["option_order_json"])]
            assistance = None
            condition = Condition(session["condition"])
            if condition != Condition.CONTROL:
                stimulus = json.loads(stored["stimulus_json"])
                recommendation = option_map[stimulus["recommendation_option_id"]]
                assistance = AssistanceView(
                    recommendation_option_id=recommendation.id,
                    recommendation_name=recommendation.name,
                    explanation=stimulus["explanation"] if condition == Condition.AI_EXPLANATION else None,
                    confidence_percent=stimulus["confidence_percent"]
                    if condition == Condition.AI_CONFIDENCE
                    else None,
                )
            return TrialView(
                id=trial.id,
                title=trial.title,
                context=trial.context,
                decision_question=trial.decision_question,
                criteria=trial.criteria,
                attribute_labels=list(trial.attribute_labels),
                options=[
                    OptionView(id=item.id, name=item.name, attributes=item.attributes)
                    for item in ordered_options
                ],
                assistance=assistance,
                trial_number=stored["trial_order"] + 1,
                total_trials=len(TRIALS),
            )

    def register_attempt(self, session_id: str, trial_id: str) -> TrialAttemptCreated:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            session = self._session(connection, session_id)
            stored = connection.execute(
                "SELECT * FROM session_trials WHERE session_id = ? AND trial_order = ?",
                (session_id, session["current_trial_index"]),
            ).fetchone()
            if (
                session["status"] != SessionStatus.IN_PROGRESS.value
                or stored is None
                or stored["trial_id"] != trial_id
            ):
                raise fail(status.HTTP_409_CONFLICT, "This trial is not active for the session.")
            attempt_count = connection.execute(
                "SELECT COUNT(*) FROM trial_attempts WHERE session_id = ? AND trial_id = ?",
                (session_id, trial_id),
            ).fetchone()[0]
            attempt_id = f"att_{secrets.token_urlsafe(18)}"
            connection.execute(
                "INSERT INTO trial_attempts(id, session_id, trial_id, attempt_number, presented_at) VALUES (?, ?, ?, ?, ?)",
                (attempt_id, session_id, trial_id, attempt_count + 1, now()),
            )
            connection.commit()
            return TrialAttemptCreated(
                attempt_id=attempt_id, trial_id=trial_id, attempt_number=attempt_count + 1
            )

    def submit_response(self, session_id: str, request: TrialResponseRequest) -> TrialResponseReceipt:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            prior = connection.execute(
                "SELECT trial_id FROM trial_responses WHERE idempotency_key = ?", (request.idempotency_key,)
            ).fetchone()
            if prior is not None:
                session = self._session(connection, session_id)
                return TrialResponseReceipt(
                    trial_id=prior["trial_id"],
                    next_status=SessionStatus(session["status"]),
                    next_trial_index=session["current_trial_index"],
                    total_trials=len(TRIALS),
                )
            session = self._session(connection, session_id)
            current = connection.execute(
                "SELECT * FROM session_trials WHERE session_id = ? AND trial_order = ?",
                (session_id, session["current_trial_index"]),
            ).fetchone()
            attempt = connection.execute(
                "SELECT * FROM trial_attempts WHERE id = ? AND session_id = ? AND trial_id = ?",
                (request.attempt_id, session_id, request.trial_id),
            ).fetchone()
            if (
                session["status"] != SessionStatus.IN_PROGRESS.value
                or current is None
                or current["trial_id"] != request.trial_id
                or attempt is None
            ):
                raise fail(status.HTTP_409_CONFLICT, "This response does not match the active trial.")
            already_saved = connection.execute(
                "SELECT 1 FROM trial_responses WHERE session_id = ? AND trial_id = ?",
                (session_id, request.trial_id),
            ).fetchone()
            if already_saved:
                raise fail(status.HTTP_409_CONFLICT, "A response for this trial has already been saved.")
            trial = trial_by_id(request.trial_id)
            valid_options = {entry.id for entry in trial.options}
            if request.selected_option_id not in valid_options:
                raise fail(
                    status.HTTP_422_UNPROCESSABLE_ENTITY, "The selected option is not part of this trial."
                )
            stimulus = json.loads(current["stimulus_json"])
            condition = Condition(session["condition"])
            followed_ai = (
                None
                if condition == Condition.CONTROL
                else request.selected_option_id == stimulus["recommendation_option_id"]
            )
            selected_correct = request.selected_option_id == trial.correct_option_id
            next_index = session["current_trial_index"] + 1
            next_status = (
                SessionStatus.QUESTIONNAIRE_PENDING
                if next_index == len(TRIALS)
                else SessionStatus.IN_PROGRESS
            )
            connection.execute(
                """INSERT INTO trial_responses
                (id, session_id, trial_id, attempt_id, selected_option_id, participant_confidence, reasoning,
                 response_time_ms, followed_ai, selected_correct_option, ai_recommendation_correct, idempotency_key, submitted_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    f"rsp_{secrets.token_urlsafe(18)}",
                    session_id,
                    request.trial_id,
                    request.attempt_id,
                    request.selected_option_id,
                    request.participant_confidence,
                    request.reasoning,
                    request.response_time_ms,
                    followed_ai,
                    selected_correct,
                    stimulus["recommendation_correct"] if condition != Condition.CONTROL else None,
                    request.idempotency_key,
                    now(),
                ),
            )
            connection.execute(
                "UPDATE study_sessions SET current_trial_index = ?, status = ? WHERE id = ?",
                (next_index, next_status.value, session_id),
            )
            connection.commit()
            return TrialResponseReceipt(
                trial_id=request.trial_id,
                next_status=next_status,
                next_trial_index=next_index,
                total_trials=len(TRIALS),
            )

    def questionnaire(self, session_id: str) -> QuestionnaireView:
        with self._connection() as connection:
            session = self._session(connection, session_id)
            if session["status"] != SessionStatus.QUESTIONNAIRE_PENDING.value:
                raise fail(
                    status.HTTP_409_CONFLICT, "The questionnaire is available after all trials are complete."
                )
            return QuestionnaireView(
                items=list(items_for(Condition(session["condition"]))),
                scale=SCALE,
                free_text_prompt="What influenced your decisions most during the study?",
            )

    def submit_questionnaire(self, session_id: str, request: QuestionnaireRequest) -> None:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            session = self._session(connection, session_id)
            expected = {item.id for item in items_for(Condition(session["condition"]))}
            if session["status"] != SessionStatus.QUESTIONNAIRE_PENDING.value:
                raise fail(status.HTTP_409_CONFLICT, "This questionnaire is not available.")
            if set(request.responses) != expected or any(
                value not in SCALE for value in request.responses.values()
            ):
                raise fail(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "Provide one valid response for each questionnaire item.",
                )
            connection.execute(
                "INSERT INTO post_study_responses(session_id, responses_json, free_text, submitted_at) VALUES (?, ?, ?, ?)",
                (session_id, json.dumps(request.responses), request.free_text, now()),
            )
            connection.execute(
                "UPDATE study_sessions SET status = ?, completed_at = ? WHERE id = ?",
                (SessionStatus.COMPLETED.value, now(), session_id),
            )
            connection.commit()

    def stop(self, session_id: str) -> None:
        with self._connection() as connection:
            session = self._session(connection, session_id)
            if session["status"] not in {
                SessionStatus.IN_PROGRESS.value,
                SessionStatus.QUESTIONNAIRE_PENDING.value,
            }:
                raise fail(status.HTTP_409_CONFLICT, "This session cannot be stopped.")
            connection.execute(
                "UPDATE study_sessions SET status = ?, completed_at = ? WHERE id = ?",
                (SessionStatus.STOPPED.value, now(), session_id),
            )

    def debrief(self, session_id: str) -> DebriefView:
        with self._connection() as connection:
            session = self._session(connection, session_id)
            if session["status"] not in {SessionStatus.COMPLETED.value, SessionStatus.STOPPED.value}:
                raise fail(status.HTTP_409_CONFLICT, "The debrief is available after completion or stopping.")
            return DebriefView(
                title="Thank you for taking part",
                paragraphs=[
                    "This study examines when people follow or reject AI-assisted recommendations while making fictional resource-selection decisions.",
                    "The recommendations were controlled research stimuli. Some were intentionally incorrect so the study can examine reliance as well as accuracy.",
                    "No live AI model generated the advice, and the scenarios did not concern real financial, medical, legal, political, or employment decisions.",
                    "Your responses are recorded without asking for identifying information. Thank you for helping us study how people interact with decision aids.",
                ],
            )

    def researcher_summary(self) -> ResearcherSummary:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT condition, COUNT(*) AS count FROM study_sessions WHERE study_version = ? GROUP BY condition",
                (STUDY_VERSION,),
            ).fetchall()
            counts = {condition: 0 for condition in Condition}
            counts.update({Condition(row["condition"]): row["count"] for row in rows})
            total = connection.execute(
                "SELECT COUNT(*) FROM study_sessions WHERE study_version = ?", (STUDY_VERSION,)
            ).fetchone()[0]
            completed = connection.execute(
                "SELECT COUNT(*) FROM study_sessions WHERE status = ?", (SessionStatus.COMPLETED.value,)
            ).fetchone()[0]
            stopped = connection.execute(
                "SELECT COUNT(*) FROM study_sessions WHERE status = ?", (SessionStatus.STOPPED.value,)
            ).fetchone()[0]
            responses = connection.execute("SELECT COUNT(*) FROM trial_responses").fetchone()[0]
            return ResearcherSummary(
                study_version=STUDY_VERSION,
                total_sessions=total,
                completed_sessions=completed,
                stopped_sessions=stopped,
                total_trial_responses=responses,
                sessions_by_condition=counts,
            )
