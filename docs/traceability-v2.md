# V2 requirements traceability matrix

V2 builds on V1 commit `bef8e6c0bfae46af486e561841c32f9c8d159b88`.
The original [V1 evaluation matrix](../traceability.md) is preserved without edits;
its satisfaction assessments describe V1, not V2. This companion matrix tracks
V2 implementation and technical checks against the revised requirements.

Evidence citations retain the original transcript key and resolved locators in
[interview-evidence.csv](../evidence/interview-evidence.csv). The revised rules are
in [003 V2 spec](../specs/003-v2-record-integrity/spec.md); unchanged rules remain
in the [002 V1 spec](../specs/002-maintenance-reliability-safety/spec.md).

| Requirement | Stakeholder evidence | Goal IDs | V1 evaluation → V2 requirement | V2 implementation | Technical check / remaining validation |
|---|---|---|---|---|---|
| REQ-01 — stop capture | T2-L63/L80; T1-L92/L83 | G1.1; G1.1.1; G1.1.2; G4.3 | F-03 → FR-024; preserve FR-001/002, refine FR-003 to one active stop | [domain.js](../frontend/domain.js): activeFor, openRecords, openFor, openEvent; [app.js](../frontend/app.js): report/sensor controls, pendingView | No-field capture and active-stop deduplication pass; new interval after good part retains older pending closeout |
| REQ-02 — downtime | T2-L9/L14/L63; T10-L13 | G1.1; G1.1.3 | F-02/F-03 → FR-023/024; retain duration arithmetic | domain.js: downtime, confirmGood; app.js: duration and operator form | Whole-minute/frozen clock checks pass; pre-release time refused; separate intervals preserved |
| REQ-03 — coded closure | T2-L16; T5-L83; T10-L13 | G1.2; G1.2.1 | Preserve FR-006/007, use strengthened dependent safety gates | domain.js: setReason, closeMissing, closeEvent; app.js: reason/closure controls | Fixed codes, early-code retention and enumerated missing-item checks pass |
| REQ-04 — repair capture | T1-L29/L81/L85; T4-L82; T9-L26 | G1.3.1; G4.1 | Preserve FR-008/009; notes do not implicitly acknowledge handover | domain.js: addEntry, stamp; app.js: note/photo form, timeline | Text, photo-only domain state, empty refusal and stamps pass; browser photo display and human SC-004 timing remain unverified |
| REQ-05 — summary/history | T1-L85; T4-L109; T7-L24; T2-L34/L40 | G1.3.2 | Preserve FR-010/011; expose active stop separately from pending closeout (F-03) | domain.js: summary, openRecords; app.js: summary, pendingView, history | Summary checks and browser separate-record navigation pass; human SC-005 comprehension remains unverified |
| REQ-06 — isolation/release | T3-L14/L50/L57; T6-L64/L81; T5-L76; T11-L14/L22 | G2.1; G2.1.1; G4.3 | F-01/F-02 → FR-021–023; strengthen FR-012–015 | domain.js: sourceApplicable, setSourceApplicable, isolationMissing, applyLock, verifyZero, removeLock, authorizeRelease, confirmGood; app.js: energyView | Historical missing verification, applicable-source omission, exclusion authority/reason, stamps, release and chronology checks pass; stakeholder safety policy remains unconfirmed |
| REQ-07 — handover | T1-L47; T10-L11; T11-L22 | G1.3.5 | F-04 → FR-025; replace latest-note eligibility in FR-016/017 | domain.js: isolationFingerprint, handover, acknowledge; app.js: handover status/control | Boundary, note persistence, role, dated-shift and critical-change checks pass; browser note does not clear overdue acknowledgment |
| REQ-08 — repair verification | T1-L34/L90; T9-L22 | G1.9 | F-03/F-05 → FR-024/026/027; strengthen FR-018/019 | domain.js: verificationEvidence, reconcileRepeats, verification; app.js: verification evidence/history/repeat links | Interrupted/complete shifts, unknown/late reason, matching/different categories and deadline checks pass; reason-code proxy still needs stakeholder confirmation |
| REQ-09 — complete records | T6-L81/L96/L98/L111 | G3.4 | F-01 → FR-021/022; strengthen FR-020 beyond active locks | domain.js: isolationMissing, closeMissing, authorizeRelease, acknowledge; app.js: retained evidence/missing-field display | Removed unverified record blocks release/closure; verified applicable active isolation can hand over; required fields remain visible |

## Assessment scope

The 24 V2 domain acceptance tests pass; selected browser workflows cover all five
findings. These establish technical behavior in a mock prototype, not full stakeholder
satisfaction or production safety. No blanket “Fully satisfied” reassessment is made
where human checks or stakeholder decisions remain outstanding. See
[v2-change-map.md](v2-change-map.md) and [saved check results](v2-evidence/).

V1's code, spec, assessment and history are preserved. V2 adds requirements refinements
and implementation on top of that baseline; it does not rewrite the original evaluation.
