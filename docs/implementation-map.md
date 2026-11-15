# V1 implementation reference (Step 3)

This source map is an aid to the later student evaluation, not a completed Step 4
traceability assessment. Evidence/goal IDs below come from the supplied 002 spec.
No stakeholder satisfaction status or learning-log reflections are asserted.

| Requirement | Evidence | Goal | frontend/domain.js | frontend/app.js behavior |
|---|---|---|---|---|
| REQ-01 | T2-L63/L80, T1-L92 | G1.1, G1.1.1/2 | openEvent, openFor | one-tap report; sensor simulation; machine selection |
| REQ-02 | T2-L9/L14, T10-L13 | G1.1.3 | confirmGood, downtime | operator confirmation, running/frozen duration |
| REQ-03 | T2-L16, T5-L83 | G1.2, G1.2.1 | setReason, closeMissing, closeEvent | fixed reason list and enumerated close refusals |
| REQ-04 | T1-L29/L81/L85, T4-L82 | G1.3.1, G4.1 | addEntry | text/photo capture with automatic author/time/shift |
| REQ-05 | T1-L85, T4-L109, T7-L24 | G1.3.2 | summary | next action, tests, people, timeline and open repair filter |
| REQ-06 | T3-L14/L50/L57, T5-L76, T11-L14/L22 | G2.1, G2.1.1 | applyLock, verifyZero, removeLock, authorizeRelease, releaseBlocked | isolation cards, retained applier/remover names and supervisor gate |
| REQ-07 | T1-L47, T10-L11, T11-L22 | G1.3.5 | shiftAt, handover, acknowledge | acknowledgment and overdue highlighting at 30 minutes |
| REQ-08 | T1-L34/L90, T9-L22 | G1.9 | verificationEnd, reconcileRepeats, verification | history, verification state, repeat links, demo clock |
| REQ-09 | T6-L96/L98/L111 | G3.4 | closeMissing, acknowledge | blocked closure and incomplete-energy handover messages |

`tests/domain.test.js` checks these transitions deterministically, including exact
boundaries, cross-user lock removal, late repeat coding, and closed-record immutability.
Transcript key and original model references: docs/goal-model.md §1 and 002 spec's
15-goal table. Human interview-evidence assurance remains part of Step 4.
