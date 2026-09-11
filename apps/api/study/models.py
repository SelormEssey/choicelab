from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

STUDY_VERSION = "CHOICELAB_STUDY_V1"
CONSENT_VERSION = "CHOICELAB_CONSENT_V1"


class Condition(StrEnum):
    CONTROL = "CONTROL"
    AI_RECOMMENDATION = "AI_RECOMMENDATION"
    AI_EXPLANATION = "AI_EXPLANATION"
    AI_CONFIDENCE = "AI_CONFIDENCE"


class SessionStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    QUESTIONNAIRE_PENDING = "QUESTIONNAIRE_PENDING"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"


@dataclass(frozen=True)
class OptionDefinition:
    id: str
    name: str
    attributes: dict[str, str]


@dataclass(frozen=True)
class TrialDefinition:
    id: str
    title: str
    context: str
    decision_question: str
    criteria: str
    attribute_labels: tuple[str, ...]
    options: tuple[OptionDefinition, ...]
    correct_option_id: str
    incorrect_ai_option_id: str
    explanation_correct: str
    explanation_incorrect: str
    confidence_correct: int
    confidence_incorrect: int
