# Core human-AI study protocol

## Research question

> How do AI recommendations, explanations, and confidence cues affect human decision-making and reliance?

This is a research-prototype protocol. It does not report recruitment, participants, findings, institutional approval, or statistical significance.

## Study design

The independent variable is the presentation of controlled decision-aid information:

| Condition         | Recommendation | Explanation | Confidence cue |
| ----------------- | -------------- | ----------- | -------------- |
| CONTROL           | No             | No          | No             |
| AI_RECOMMENDATION | Yes            | No          | No             |
| AI_EXPLANATION    | Yes            | Yes         | No             |
| AI_CONFIDENCE     | Yes            | No          | Yes            |

Each participant is assigned by the backend to one condition and one of two complementary stimulus schedules. Assignment balances created sessions within the current study version. Participants cannot select their own condition.

## Stimuli and trials

The study contains ten versioned fictional software and resource-selection scenarios. Each exposes the stated criteria, comparable attributes, and two or three options. Every scenario has one uniquely preferable option under its stated criteria.

Advice comes from controlled fixtures, not a live model. Each schedule contains five correct and five intentionally incorrect recommendations. Complementary schedules reverse recommendation correctness by trial position so advice correctness is not fixed to a particular scenario order. Trial order, option order, assigned schedule, study version, and fixture checksum are persisted when consent creates a session.

## Measures

- Decision accuracy: whether the selected option satisfies the scenario's defined answer key.
- AI following: agreement with displayed advice. This is null in CONTROL.
- Appropriate reliance: following correct advice or rejecting incorrect advice, interpreted alongside decision accuracy.
- Over-reliance: following intentionally incorrect advice.
- Under-reliance: rejecting correct advice.
- Participant confidence: required 0 to 100 rating after each decision.
- Response time: milliseconds from usable trial presentation to submission, with re-entry recorded as a separate attempt.
- Post-study perceptions: condition-appropriate Likert responses and optional free text.

Agreement by itself does not prove that displayed advice changed a decision. This prototype has no pre-advice baseline.

## Consent, privacy, and debriefing

Explicit consent is required before a session exists. The study requests no name, email, account, phone number, demographic identity, or sensitive decision data. It does not use analytics, fingerprinting, behavioral advertising, or IP collection logic.

Participation is voluntary. A participant can irreversibly stop, after which trial progress is blocked and a debrief explains the controlled stimuli and intentional inaccuracies. Completed participants receive the same debrief. Responses are stored locally in a backend-owned SQLite database for this prototype.

## Limitations

The scenarios are fictional and low risk. Advice reliability, explanations, and confidence cues are artificial controlled stimuli rather than calibrated model output. Local anonymous session URLs are resumable secrets, not authenticated identities. Browser response timing is useful instrumentation but is not tamper-proof and can include interruption or reading time.
