# Ethics and privacy

## Principle

Decision-support interactions can involve uncertainty, unequal access to resources, and meaningful perceptions of authority. ChoiceLab will treat participants as decision-makers with context and values, not as inputs to optimize.

## Current data posture

The prototype stores consented anonymous study sessions, fictional-scenario responses, required confidence ratings, optional bounded reasoning, timing, and post-study responses in a local backend-owned SQLite database. It does not collect names, contact details, accounts, personal records, demographic identity, IP addresses, or analytics data.

## Controlled manipulation and debriefing

The prototype presents controlled decision-aid stimuli. Some advice is intentionally incorrect so the study can examine appropriate reliance, over-reliance, and rejection of advice. This manipulation is disclosed only in the debrief to avoid changing trial behavior. A participant may stop at any time; stopping ends the session before the debrief is shown.

## Planning commitments

- Collect only data needed to address a documented research question.
- Avoid collecting identifiers, credentials, personal records, or detailed histories unless a future protocol provides a specific and approved need.
- Explain what data is collected, why it is collected, how it will be used, and how long it will be retained.
- Separate contact information from research data where feasible.
- Protect stored research data using institutionally appropriate access controls.
- Make it clear that participation is voluntary and that the fictional study scenarios are not real-world advice.
- Consider how explanations, prompts, and defaults could influence a participant's choices.

## Risks to assess before research begins

- Discomfort or stress caused by uncertainty, performance, or AI assistance.
- Unintended disclosure of sensitive information in optional free-text reasoning.
- Misinterpretation of a fictional study scenario as real-world advice.
- Power dynamics during recruitment, facilitation, and interpretation.
- Overstating what a prototype or study result can demonstrate.

## TODO

- [ ] Determine applicable institutional review requirements.
- [ ] Write an explicit data retention and deletion schedule.
- [ ] Define incident response and participant support procedures where required.
- [ ] Review consent language with the course instructor or ethics reviewer.
