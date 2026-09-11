# ChoiceLab

ChoiceLab is a graduate-level Human-Computer Interaction research platform for studying how AI recommendations, explanations, and confidence cues influence human decision-making and reliance.

The core study is a local research prototype. It uses fictional software and resource-selection decisions, controlled experimental stimuli, anonymous sessions, and no external AI service.

## Project focus

Decision aids can influence what people select, trust, and rely on. ChoiceLab tests information presentation while keeping every scenario fictional and low risk.

The current provisional research question is:

> How do AI recommendations, explanations, and confidence cues affect human decision-making and reliance?

No participants, findings, or statistical claims are represented in this repository.

## Core study

Participant flow: landing page → study introduction → consent → ten trials → post-study questionnaire → debrief. Participants may stop at any time; stopping permanently ends the session before debriefing.

The backend assigns one of four conditions: `CONTROL`, `AI_RECOMMENDATION`, `AI_EXPLANATION`, or `AI_CONFIDENCE`. Five recommendations per schedule are correct and five are intentionally incorrect. The browser never receives answer keys or recommendation-correctness fields before a response is saved.

```text
Next.js participant interface → FastAPI study service → SQLite
                               ↓
                 controlled, versioned study fixtures
```

SQLite is local, backend-owned prototype storage. Its repository boundary is designed for a later PostgreSQL replacement. The system requests no identity or contact data, does not use tracking, and does not call a live AI API.

## Project status

| Area        | Current focus                                                                    |
| ----------- | -------------------------------------------------------------------------------- |
| Research    | Controlled human-AI reliance study protocol and data dictionary.                 |
| Design      | Accessible participant decision flow with restrained condition presentation.     |
| Development | Next.js participant experience, FastAPI study API, and local SQLite persistence. |
| Evaluation  | Analysis-ready response data. Formal evaluation remains future work.             |

## Repository structure

    apps/

web/ Next.js landing page and participant study routes
api/ FastAPI study service and SQLite repository boundary
docs/
research/ Study protocol, data dictionary, and research framing
design/ Design requirements and accessibility guidance
evaluation/ Evaluation planning

## Local development

### Web

Requirements: Node.js 20.9 or newer and npm.

    npm install
    npm run dev

The landing page is served by Next.js at the local URL printed in the terminal.

### API

Requirements: Python 3.10 or newer.

    cd apps/api
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload

The API preserves `GET /health` and `GET /v1/project-status`. Study routes live under `/v1/study/`.

### Researcher summary configuration

`GET /v1/study/researcher-summary` is disabled by default and remains excluded from OpenAPI documentation. It returns a 404 unless a local researcher explicitly enables it before starting the API:

    CHOICELAB_ENABLE_RESEARCHER_SUMMARY=true uvicorn main:app --reload

Recognized enabled values are `1`, `true`, `yes`, and `on`, case-insensitively. All other values, including an unset value, leave the endpoint unavailable. When enabled, it returns aggregate counts only; it is not intended as a public production endpoint.

## Roadmap

1. Pilot the controlled study materials with an approved protocol.
2. Review accessibility with relevant assistive technologies.
3. Prepare PostgreSQL deployment only if the study scope requires it.
4. Conduct a documented evaluation.
5. Report findings, limitations, and design iterations responsibly.

## Research integrity

ChoiceLab will not represent assumptions as evidence. The repository does not contain fabricated participants, interview responses, survey data, usability results, or personas. Research findings will be added only when they are collected, analyzed, and documented.

## License

ChoiceLab is available under the [MIT License](LICENSE).
