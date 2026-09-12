from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .models import Condition, SessionStatus


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ConsentRequest(StrictModel):
    consent: Literal[True]


class SessionCreated(StrictModel):
    session_id: str
    session_token: str
    anonymous_participant_id: str
    status: SessionStatus
    study_version: str


class SessionProgress(StrictModel):
    session_id: str
    status: SessionStatus
    current_trial_index: int
    total_trials: int
    study_version: str
    started_at: datetime
    completed_at: datetime | None = None


class OptionView(StrictModel):
    id: str
    name: str
    attributes: dict[str, str]


class AssistanceView(StrictModel):
    recommendation_option_id: str
    recommendation_name: str
    explanation: str | None = None
    confidence_percent: int | None = None


class TrialView(StrictModel):
    id: str
    title: str
    context: str
    decision_question: str
    criteria: str
    attribute_labels: list[str]
    options: list[OptionView]
    assistance: AssistanceView | None = None
    trial_number: int
    total_trials: int


class TrialAttemptRequest(StrictModel):
    trial_id: str = Field(min_length=1, max_length=80)


class TrialAttemptCreated(StrictModel):
    attempt_id: str
    trial_id: str
    attempt_number: int


class TrialResponseRequest(StrictModel):
    trial_id: str = Field(min_length=1, max_length=80)
    attempt_id: str = Field(min_length=20, max_length=80)
    selected_option_id: str = Field(min_length=1, max_length=80)
    participant_confidence: int = Field(ge=0, le=100)
    reasoning: str | None = Field(default=None, max_length=800)
    response_time_ms: int = Field(ge=100, le=3_600_000)
    idempotency_key: str = Field(min_length=16, max_length=120)

    @field_validator("reasoning")
    @classmethod
    def strip_reasoning(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class TrialResponseReceipt(StrictModel):
    trial_id: str
    next_status: SessionStatus
    next_trial_index: int
    total_trials: int


class QuestionnaireItem(StrictModel):
    id: str
    statement: str


class QuestionnaireView(StrictModel):
    items: list[QuestionnaireItem]
    scale: dict[int, str]
    free_text_prompt: str


class QuestionnaireRequest(StrictModel):
    responses: dict[str, int]
    free_text: str | None = Field(default=None, max_length=1000)

    @field_validator("free_text")
    @classmethod
    def strip_free_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class DebriefView(StrictModel):
    title: str
    paragraphs: list[str]


class ResearcherSummary(StrictModel):
    study_version: str
    total_sessions: int
    completed_sessions: int
    stopped_sessions: int
    total_trial_responses: int
    sessions_by_condition: dict[Condition, int]
