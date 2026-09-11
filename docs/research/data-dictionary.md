# Core study data dictionary

## Session

| Field                      | Meaning                                                            |
| -------------------------- | ------------------------------------------------------------------ |
| `id`                       | Opaque session identifier used to resume a study.                  |
| `anonymous_participant_id` | Random non-identifying study label.                                |
| `condition`                | Backend-assigned interface condition.                              |
| `schedule_id`              | Complementary controlled-stimulus schedule.                        |
| `study_version`            | `CHOICELAB_STUDY_V1`.                                              |
| `fixture_checksum`         | Identifier for the fixture definition used at session creation.    |
| `status`                   | `IN_PROGRESS`, `QUESTIONNAIRE_PENDING`, `COMPLETED`, or `STOPPED`. |

## Trial response

| Field                       | Meaning                                                                 |
| --------------------------- | ----------------------------------------------------------------------- |
| `selected_option_id`        | Active choice selected by the participant.                              |
| `participant_confidence`    | Required 0 to 100 self-reported confidence.                             |
| `reasoning`                 | Optional short text, bounded to 800 characters.                         |
| `response_time_ms`          | Final presentation attempt duration in milliseconds.                    |
| `followed_ai`               | Server-derived agreement with shown advice; null for CONTROL.           |
| `selected_correct_option`   | Server-derived decision accuracy.                                       |
| `ai_recommendation_correct` | Private fixture-derived accuracy of displayed advice; null for CONTROL. |
| `trial_order`               | Persisted presentation order for the session.                           |

## Post-study response

Likert responses use 1 for strongly disagree through 5 for strongly agree. Assisted conditions receive AI-perception items. CONTROL receives comparison-interface items. The optional free-text response is bounded to 1,000 characters.
