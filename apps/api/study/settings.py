import os

RESEARCHER_SUMMARY_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})


def researcher_summary_enabled() -> bool:
    """Return whether local researcher summary access was explicitly enabled."""
    value = os.getenv("CHOICELAB_ENABLE_RESEARCHER_SUMMARY", "")
    return value.strip().lower() in RESEARCHER_SUMMARY_TRUE_VALUES
