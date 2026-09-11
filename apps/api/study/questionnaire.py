from __future__ import annotations

from .models import Condition
from .schemas import QuestionnaireItem

SCALE = {1: "Strongly disagree", 2: "Disagree", 3: "Neutral", 4: "Agree", 5: "Strongly agree"}

ASSISTED_ITEMS = (
    QuestionnaireItem(id="clarity", statement="The decision aid presented information clearly."),
    QuestionnaireItem(id="usefulness", statement="The decision aid was useful for completing the scenarios."),
    QuestionnaireItem(id="trust", statement="I trusted the decision aid during the study."),
    QuestionnaireItem(id="reliability", statement="The decision aid seemed reliable."),
    QuestionnaireItem(id="comfort", statement="I felt comfortable relying on the decision aid."),
    QuestionnaireItem(
        id="future_use", statement="I would consider using similar decision assistance in the future."
    ),
    QuestionnaireItem(id="fallibility_awareness", statement="I was aware that a decision aid can be wrong."),
)

CONTROL_ITEMS = (
    QuestionnaireItem(id="clarity", statement="The scenario information was presented clearly."),
    QuestionnaireItem(
        id="sufficiency", statement="The scenario information was sufficient to make decisions."
    ),
    QuestionnaireItem(id="effort", statement="Comparing the options required a reasonable amount of effort."),
    QuestionnaireItem(id="control", statement="I felt in control of my decisions during the study."),
    QuestionnaireItem(
        id="future_use", statement="I would consider using a similar comparison interface in the future."
    ),
)


def items_for(condition: Condition) -> tuple[QuestionnaireItem, ...]:
    return CONTROL_ITEMS if condition == Condition.CONTROL else ASSISTED_ITEMS
