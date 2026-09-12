# Heuristic evaluation

## Status

This document reports an expert review of the ChoiceLab prototype conducted on September 12, 2026. It is not a usability study, does not involve participants, and does not support claims about user behavior or experimental outcomes.

## Method

The participant journey was reviewed from landing page through consent, ten decision trials, the post-study questionnaire, and debrief. The review used Nielsen-style usability heuristics together with checks drawn from WCAG 2.2 principles: clear system status, user control, consistency, error recovery, semantic structure, keyboard-operable controls, visible focus, and non-color-only communication.

Automated checks supplement the review. API tests cover study integrity and access control. Playwright covers the complete browser journey and verifies that a session URL cannot be resumed without its generated browser token.

## Findings and implemented responses

| Area                   | Observation                                                                   | Response                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Study status           | Trial count and progress were already visible.                                | Retained the text label and semantic `progress` element.                                    |
| User control           | Participants can stop, but stopping is irreversible.                          | Retained the explicit confirmation and immediate debrief.                                   |
| Research transparency  | A public prototype could be mistaken for an active study.                     | Added a demo-mode notice that says submissions are not research data.                       |
| Session privacy        | A session identifier in the URL previously acted as the only access secret.   | Added a separate generated token stored in the browser session and hashed in the database.  |
| Error recovery         | API failures produce a readable message and retry path during trials.         | Added end-to-end verification of the primary journey; offline recovery remains future work. |
| Experimental integrity | Browser responses could expose answer keys or assignment logic.               | Confirmed that scoring fields stay on the server and added automated checks.                |
| Accessibility          | Forms use fieldsets, legends, labels, native inputs, and non-color-only text. | Preserved semantic controls; assistive-technology testing is still required.                |

## Remaining risks

- Session tokens live in session storage and are not a replacement for a full authenticated research platform.
- Browser timing includes reading time, interruptions, and device variability.
- The researcher summary must remain disabled on public deployments until protected access exists.
- Keyboard and screen-reader behavior still needs hands-on testing with relevant assistive technologies.
- The fictional scenarios and questionnaire require review before any approved participant study.

## Conclusion

The prototype communicates its experimental status, protects session actions beyond a guessable or shared URL, and provides a coherent consent-to-debrief journey. The next evaluation milestone should be a documented accessibility review followed by a small pilot only after appropriate academic or institutional review.
