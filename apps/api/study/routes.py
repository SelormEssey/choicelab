from fastapi import APIRouter, Depends, HTTPException, Response, status

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
from .settings import researcher_summary_enabled

router = APIRouter(prefix="/v1/study", tags=["study"])


def get_service() -> StudyService:
    return StudyService()


@router.post("/sessions", response_model=SessionCreated, status_code=status.HTTP_201_CREATED)
def create_session(request: ConsentRequest, service: StudyService = Depends(get_service)) -> SessionCreated:
    return service.create_session()


@router.get("/sessions/{session_id}", response_model=SessionProgress)
def get_session(session_id: str, service: StudyService = Depends(get_service)) -> SessionProgress:
    return service.progress(session_id)


@router.get("/sessions/{session_id}/current-trial", response_model=TrialView)
def get_current_trial(session_id: str, service: StudyService = Depends(get_service)) -> TrialView:
    return service.current_trial(session_id)


@router.post(
    "/sessions/{session_id}/trial-attempts",
    response_model=TrialAttemptCreated,
    status_code=status.HTTP_201_CREATED,
)
def create_trial_attempt(
    session_id: str, request: TrialAttemptRequest, service: StudyService = Depends(get_service)
) -> TrialAttemptCreated:
    return service.register_attempt(session_id, request.trial_id)


@router.post("/sessions/{session_id}/responses", response_model=TrialResponseReceipt)
def submit_response(
    session_id: str, request: TrialResponseRequest, service: StudyService = Depends(get_service)
) -> TrialResponseReceipt:
    return service.submit_response(session_id, request)


@router.get("/sessions/{session_id}/questionnaire", response_model=QuestionnaireView)
def get_questionnaire(session_id: str, service: StudyService = Depends(get_service)) -> QuestionnaireView:
    return service.questionnaire(session_id)


@router.post("/sessions/{session_id}/post-study", status_code=status.HTTP_204_NO_CONTENT)
def submit_questionnaire(
    session_id: str, request: QuestionnaireRequest, service: StudyService = Depends(get_service)
) -> Response:
    service.submit_questionnaire(session_id, request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/sessions/{session_id}/stop", status_code=status.HTTP_204_NO_CONTENT)
def stop_session(session_id: str, service: StudyService = Depends(get_service)) -> Response:
    service.stop(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/sessions/{session_id}/debrief", response_model=DebriefView)
def get_debrief(session_id: str, service: StudyService = Depends(get_service)) -> DebriefView:
    return service.debrief(session_id)


@router.get("/researcher-summary", response_model=ResearcherSummary, include_in_schema=False)
def researcher_summary(service: StudyService = Depends(get_service)) -> ResearcherSummary:
    if not researcher_summary_enabled():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return service.researcher_summary()
