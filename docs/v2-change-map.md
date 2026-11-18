# Step 5 — V2 technical change map

Date: 2026-11-18. Input matrix: ../traceability.md, preserved verbatim.
V1 baseline: bef8e6c. Specification-first commit: 2177b9f.
This is implementation/verification documentation, not the student-authored learning log.

| Finding | V2 requirement revision | Goal/evidence | Implementation | Verification |
|---|---|---|---|---|
| F-01 | FR-021/022; REQ-06/09 | G2.1/G2.1.1/G3.4; T3-L14, T6-L64/L81/L98/L111 | domain.js: sourceApplicable, setSourceApplicable, isolationMissing, authorizeRelease, acknowledge, closeEvent; app.js: source forms, per-cycle evidence and missing list | Domain checks for removed unverified locks, absent applicable sources, supervisor exclusion, immutable history, valid active handover; browser release refusal and stamped exclusion exercised |
| F-02 | FR-023; REQ-02/06 | G1.1.3/G2.1.1; T2-L9/L14, T11-L14/L22 | domain.js: confirmGood, verifyZero, removeLock, authorizeRelease | Domain release-time boundary and relock checks; browser rejects 06:50 production after 07:40 release |
| F-03 | FR-024; REQ-01/02/08 | G1.1/G1.1.1/G1.1.3/G1.9; T2-L14/L16/L63/L80 | domain.js: activeFor, openRecords, openFor, openEvent; app.js: Pending closeout and previous-stop links | Domain new interval/active deduplication/old closure checks; browser retains prior 15-minute record and starts a separate active stop |
| F-04 | FR-025; REQ-07 | G1.3.5; T1-L47, T10-L11, T11-L22 | domain.js: handover, isolationFingerprint, acknowledge | Domain 06:29/06:30, notes, subsequent shifts and critical-change checks; browser current-shift note retains Not acknowledged, explicit acceptance clears it |
| F-05 | FR-026/027; REQ-08 | G1.9; T1-L34/L90, T9-L22 | domain.js: verificationEvidence, reconcileRepeats, verification; app.js: evidence panel/history | Domain interrupted/uninterrupted shifts, unknown/late code, matching/different repeat, exact boundaries; browser ongoing different-code stop leaves prior repair awaiting full operating evidence |

## Preservation and approvals

The user explicitly selected all five findings and approved the mock defaults.
Approval is for prototype rules, not evidence of agreement from Rob/Angela/Teo.
The 002 V1 spec and artifacts remain unchanged; new 003 spec contains the V2 delta.
V1 app bytes are copied from bef8e6c and checked against versions/v1/checksums.json.
The local v2 history descends from v1, with specification changes committed before code.

C-2 still uses a single downtime clock including LOTO hold; accounting policy remains
unresolved. Reason-code recurrence remains a limited proxy for fault identity.
Source applicability, verifier/remover authority and corrections require real stakeholder
confirmation. An unverified removed lock stays visibly incomplete; no false backfill
is provided. Real login, machine control, sensors, persistence and offline sync remain out.

## Verification facts and limits

- 24 V2 Node acceptance-rule tests passed. The original 15 V1 tests remain available
  in step4-evaluation/source-snapshot/tests and pass against the preserved V1 module.
- Static build and Pages packaging pass. Both routes were opened in-browser.
- Browser checks covered all five findings; raw selected snapshots are in v2-evidence/.
  These are technical checks, not human usability or real-world safety validation.
- Browser photo selection/display was not retested; its earlier environment block is
  retained as an outstanding check. Text and photo-only domain regression checks pass.
- Human participant SC-004 entry time and SC-005 comprehension remain outstanding.
- No learning-log text or personal reflections were generated. No push or deployment
  was performed in this V2 implementation session, per the user's local-only preference.

## Assignment completion still requiring the team

Step 5 code/spec/model work is preserved locally. Push the v2 branch and publish
both URLs when ready. The default branch README must then expose V1/V2 source,
both live prototypes, and the team-authored requirements/learning document. Complete
roles/contributions, remaining human checks and stakeholder confirmations honestly;
do not substitute these tests for those activities. See github-pages.md for hosting.
