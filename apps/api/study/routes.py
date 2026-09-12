import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Response, status

from .schemas import (
    ConsentRequest,
    DebriefView,
    QuestionnaireRequest,
    QuestionnaireView,
    ResearcherSummary,
    SessionCreated,
    SessionProgress,
    TrialAttemptCreated,
    TrialAttemptRequest,
    TrialResponseReceipt,
    TrialResponseRequest,
    TrialView,
)
from .service import StudyService
from .settings import researcher_summary_enabled, researcher_token

router = APIRouter(prefix="/v1/study", tags=["study"])


def get_service() -> StudyService:
    return StudyService()


def authorized_service(
    session_id: str,
    session_token: Annotated[str | None, Header(alias="X-Session-Token")] = None,
    service: StudyService = Depends(get_service),
) -> StudyService:
    service.authorize(session_id, session_token)
    return service


@router.post("/sessions", response_model=SessionCreated, status_code=status.HTTP_201_CREATED)
def create_session(request: ConsentRequest, service: StudyService = Depends(get_service)) -> SessionCreated:
    return service.create_session()


@router.get("/sessions/{session_id}", response_model=SessionProgress)
def get_session(session_id: str, service: StudyService = Depends(authorized_service)) -> SessionProgress:
    return service.progress(session_id)


@router.get("/sessions/{session_id}/current-trial", response_model=TrialView)
def get_current_trial(session_id: str, service: StudyService = Depends(authorized_service)) -> TrialView:
    return service.current_trial(session_id)


@router.post(
    "/sessions/{session_id}/trial-attempts",
    response_model=TrialAttemptCreated,
    status_code=status.HTTP_201_CREATED,
)
def create_trial_attempt(
    session_id: str, request: TrialAttemptRequest, service: StudyService = Depends(authorized_service)
) -> TrialAttemptCreated:
    return service.register_attempt(session_id, request.trial_id)


@router.post("/sessions/{session_id}/responses", response_model=TrialResponseReceipt)
def submit_response(
    session_id: str, request: TrialResponseRequest, service: StudyService = Depends(authorized_service)
) -> TrialResponseReceipt:
    return service.submit_response(session_id, request)


@router.get("/sessions/{session_id}/questionnaire", response_model=QuestionnaireView)
def get_questionnaire(session_id: str, service: StudyService = Depends(authorized_service)) -> QuestionnaireView:
    return service.questionnaire(session_id)


@router.post("/sessions/{session_id}/post-study", status_code=status.HTTP_204_NO_CONTENT)
def submit_questionnaire(
    session_id: str, request: QuestionnaireRequest, service: StudyService = Depends(authorized_service)
) -> Response:
    service.submit_questionnaire(session_id, request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/sessions/{session_id}/stop", status_code=status.HTTP_204_NO_CONTENT)
def stop_session(session_id: str, service: StudyService = Depends(authorized_service)) -> Response:
    service.stop(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/sessions/{session_id}/debrief", response_model=DebriefView)
def get_debrief(session_id: str, service: StudyService = Depends(authorized_service)) -> DebriefView:
    return service.debrief(session_id)


@router.get("/researcher-summary", response_model=ResearcherSummary, include_in_schema=False)
def researcher_summary(
    researcher_access_token: Annotated[
        str | None, Header(alias="X-Researcher-Token")
    ] = None,
    service: StudyService = Depends(get_service),
) -> ResearcherSummary:
    expected = researcher_token()
    if (
        not researcher_summary_enabled()
        or not expected
        or not researcher_access_token
        or not secrets.compare_digest(expected, researcher_access_token)
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return service.researcher_summary()
