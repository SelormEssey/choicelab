# ChoiceLab

ChoiceLab is a graduate-level Human-Computer Interaction project exploring how intelligent financial interfaces can support human decision-making without replacing human judgment.

The project is in an early research and development phase. It does not provide financial advice, recommendations, account connections, or automated decisions.

## Project focus

Many financial tools are designed to produce an answer quickly. ChoiceLab investigates another interaction direction: helping people examine the assumptions, consequences, and tradeoffs that shape a decision before they act.

The current provisional research question is:

> How does reflection-first intelligent assistance affect users' understanding, perceived agency, and trust compared with recommendation-first assistance during financial decision-making?

This question is provisional. It will be refined through formative research before evaluative claims or product decisions are made.

## Project status

| Area | Current focus |
| --- | --- |
| Research | Define the problem space, conduct formative research, and refine the research question. |
| Design | Turn research insights into traceable design requirements and interaction concepts. |
| Development | Establish a minimal web and API foundation. No decision-support experience is implemented. |
| Evaluation | Plan a comparative study after a research-grounded prototype is available. |

## Repository structure

    apps/
      web/                 Next.js research landing page
      api/                 FastAPI project metadata service
    docs/
      research/            Research framing and study preparation
      design/              Design requirements and accessibility guidance
      evaluation/          Evaluation planning

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

The API exposes `GET /health` and `GET /v1/project-status`. These endpoints are intentionally limited to non-sensitive project metadata.

## Roadmap

1. Conduct formative research and document methods, decisions, and limitations.
2. Refine the research question and derive evidence-backed design requirements.
3. Prototype recommendation-first and reflection-first conditions.
4. Conduct a planned comparative evaluation.
5. Report findings, limitations, and design iterations responsibly.

## Research integrity

ChoiceLab will not represent assumptions as evidence. The repository does not contain fabricated participants, interview responses, survey data, usability results, or personas. Research findings will be added only when they are collected, analyzed, and documented.

## License

ChoiceLab is available under the [MIT License](LICENSE).
