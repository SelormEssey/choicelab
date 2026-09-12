from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[1] / "data" / "choicelab.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_versions (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS study_sessions (
  id TEXT PRIMARY KEY, access_token_hash TEXT NOT NULL, anonymous_participant_id TEXT NOT NULL UNIQUE, condition TEXT NOT NULL,
  schedule_id TEXT NOT NULL, status TEXT NOT NULL, study_version TEXT NOT NULL,
  fixture_checksum TEXT NOT NULL, consent_version TEXT NOT NULL, consented_at TEXT NOT NULL,
  started_at TEXT NOT NULL, completed_at TEXT, current_trial_index INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS session_trials (
  id INTEGER PRIMARY KEY, session_id TEXT NOT NULL REFERENCES study_sessions(id) ON DELETE CASCADE,
  trial_id TEXT NOT NULL, trial_order INTEGER NOT NULL, option_order_json TEXT NOT NULL,
  stimulus_json TEXT NOT NULL, UNIQUE(session_id, trial_id), UNIQUE(session_id, trial_order)
);
CREATE TABLE IF NOT EXISTS trial_attempts (
  id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES study_sessions(id) ON DELETE CASCADE,
  trial_id TEXT NOT NULL, attempt_number INTEGER NOT NULL, presented_at TEXT NOT NULL,
  UNIQUE(session_id, trial_id, attempt_number)
);
CREATE TABLE IF NOT EXISTS trial_responses (
  id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES study_sessions(id) ON DELETE CASCADE,
  trial_id TEXT NOT NULL, attempt_id TEXT NOT NULL REFERENCES trial_attempts(id), selected_option_id TEXT NOT NULL,
  participant_confidence INTEGER NOT NULL, reasoning TEXT, response_time_ms INTEGER NOT NULL,
  followed_ai INTEGER, selected_correct_option INTEGER NOT NULL, ai_recommendation_correct INTEGER,
  idempotency_key TEXT NOT NULL UNIQUE, submitted_at TEXT NOT NULL,
  UNIQUE(session_id, trial_id)
);
CREATE TABLE IF NOT EXISTS post_study_responses (
  session_id TEXT PRIMARY KEY REFERENCES study_sessions(id) ON DELETE CASCADE,
  responses_json TEXT NOT NULL, free_text TEXT, submitted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_study_sessions_version_condition ON study_sessions(study_version, condition);
CREATE INDEX IF NOT EXISTS idx_session_trials_current ON session_trials(session_id, trial_order);
CREATE INDEX IF NOT EXISTS idx_trial_responses_session ON trial_responses(session_id);
"""


def database_path() -> Path:
    return Path(os.environ.get("CHOICELAB_DATABASE_PATH", DEFAULT_DATABASE_PATH))


def connect(path: Path | None = None) -> sqlite3.Connection:
    resolved = path or database_path()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(resolved, timeout=5, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    return connection


def initialize(path: Path | None = None) -> None:
    with connect(path) as connection:
        connection.executescript(SCHEMA)
        columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(study_sessions)").fetchall()
        }
        if "access_token_hash" not in columns:
            connection.execute("ALTER TABLE study_sessions ADD COLUMN access_token_hash TEXT")
        connection.execute(
            "INSERT OR IGNORE INTO schema_versions(version, applied_at) VALUES (1, datetime('now'))"
        )
        connection.execute("PRAGMA optimize")
