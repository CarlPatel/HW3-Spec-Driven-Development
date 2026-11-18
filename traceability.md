# Step 4 — Requirements traceability matrix

Evaluated November 15, 2026 • Repository V1 commit `bef8e6c0bfae46af486e561841c32f9c8d159b88` • [Live prototype](https://carlpatel.github.io/HW3-Spec-Driven-Development/v1/)

Baseline: the repository’s **002 specification**, with REQ-01–09 and its 15 selected goal IDs. The earlier local 20-goal overview and spec 001 are not substituted for the goals/spec used to build this V1.

Status meaning: **Fully satisfied** means the evaluated requirement’s scoped checks are supported by observed behavior and/or the pinned unit tests. **Partially satisfied** means useful behavior exists but a stated stakeholder goal is undermined or necessary validation is still missing. It does not automatically mean a coding defect. There are no Not satisfied rows because all nine requirements have implemented behavior. Assessment is limited to this mock prototype and checked paths.

Evidence columns use the repository transcript key. Every listed citation has been resolved to a raw CSV Stakeholder row and UTC timestamp in [interview-evidence.csv](evidence/interview-evidence.csv). This establishes source provenance; the proposed defaults and interpretations still require team/stakeholder review.

| Requirement / FRs | Interview evidence | Goal IDs | Implementation | Satisfaction status |
|---|---|---|---|---|
| REQ-01: Open sensor/manual event without other fields<br>FR-001–003 | T2-L63 T2-L80 T1-L92 T1-L83 | G1.1; G1.1.1; G1.1.2; G4.3 | [openEvent; openFor](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L41)<br>machine report and sensor buttons; render/bind | **Partially satisfied** |
| REQ-02: Measure stop-to-first-good-part downtime<br>FR-004–005 | T2-L9 T2-L14 T2-L63 T10-L13 | G1.1; G1.1.3 | [downtime; confirmGood](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L47)<br>duration card; good-form | **Partially satisfied** |
| REQ-03: Complete coded closure and missing-item messages<br>FR-006–007 | T2-L16 T5-L83 T10-L13 | G1.2; G1.2.1 | [setReason; closeMissing; closeEvent](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L48)<br>reason-form; Close event; status notice | **Fully satisfied** |
| REQ-04: Attributable open-repair notes and optional photo<br>FR-008–009 | T1-L29 T1-L81 T1-L85 T4-L82 T9-L26 | G1.3.1; G4.1 | [addEntry; stamp](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L62)<br>entry-form; photo handler; timeline | **Partially satisfied** |
| REQ-05: Machine summary, history and open-repair list<br>FR-010–011 | T1-L85 T4-L109 T7-L24 T2-L34 T2-L40 | G1.3.2 | [summary; openFor; verification](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L63)<br>render list; summary-grid; handover; timeline; history | **Partially satisfied** |
| REQ-06: Energy-source locks and documented release gate<br>FR-012–015 | T3-L14 T3-L50 T3-L57 T6-L64 T6-L81 T5-L76 T11-L14 T11-L22 | G2.1; G2.1.1; G4.3 | [applyLock; verifyZero; removeLock; authorizeRelease; releaseBlocked](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L55)<br>energy cards; release notice; good-form | **Partially satisfied** |
| REQ-07: Incoming-shift acknowledgment and deadline<br>FR-016–017 | T1-L47 T10-L11 T11-L22 | G1.3.5 | [shiftAt; workTime; handover; acknowledge](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L64)<br>handover button/status; overdue list class | **Partially satisfied** |
| REQ-08: Next-full-shift verification and repeat links<br>FR-018–019 | T1-L34 T1-L90 T9-L22 | G1.9 | [verificationEnd; reconcileRepeats; verification](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L68)<br>history and verification badge; repeat link; clock | **Partially satisfied** |
| REQ-09: Prevent incomplete-lockout closure and handover<br>FR-020 | T6-L81 T6-L96 T6-L98 T6-L111 | G3.4 | [closeMissing; releaseBlocked; acknowledge](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L52)<br>closure missing-item list; acknowledgment notice | **Partially satisfied** |

## Observed behavior and basis for each status

### REQ-01 — Open sensor/manual event without other fields

Manual sensorless event opens; source is manual – no sensor; simulated duplicate stop reuses the event. A genuinely new stop after first good part is also reused while the original record awaits closure.

**Basis:** Nominal FR behavior observed; event lifecycle loses a resumed-then-stopped interval (F-03).

**Checks:** UI-09; UI-18; UI-19; existing REQ-01 test; PROBE-03. **Findings:** F-03.

### REQ-02 — Measure stop-to-first-good-part downtime

Running duration advances by 30 minutes; confirmation freezes it at 30; early/future timestamps are refused. A timestamp during the recorded isolation interval is accepted once release exists at the current time.

**Basis:** Arithmetic passes; accepted chronology can contradict the release record (F-02), and a second interval can be lost (F-03).

**Checks:** UI-07; UI-13–16; UI-19; existing REQ-02 test; PROBE-02/03. **Findings:** F-02; F-03.

### REQ-03 — Complete coded closure and missing-item messages

Missing reason and first good part are enumerated; fixed-list codes are enforced; a valid timed and coded record closes. Existing tests also cover early code retention and release-dependent closure.

**Basis:** Fully satisfied for the evaluated coded-closure rule as written. This is not a claim that the incomplete safety policy in REQ-06/09 is sufficient.

**Checks:** UI-10; UI-17; existing REQ-03 and REQ-06/09 tests. **Findings:** Dependent safety limitations: F-01/F-02.

### REQ-04 — Attributable open-repair notes and optional photo

Empty entry is refused; tests and next action save with author/time/shift and appear in the timeline. Photo-only domain state passes an existing unit test; actual browser file selection/display was not tested.

**Basis:** Text workflow validated. Photo browser selection was blocked by extension file-access permission (UI-31); human SC-004 timing remains unvalidated. Neither is an application test failure.

**Checks:** UI-11; UI-12; UI-31 (environment blocked); existing REQ-04/05 test; source inspection. **Findings:** Validation remaining: photo browser path; SC-004.

### REQ-05 — Machine summary, history and open-repair list

Next action, previous tests, contributors, last-entry identity/shift and acknowledgment state are visible; closed records show verification state and history. The Open repairs filter was exercised: only Press 12 and Molder 8 remained; All machines restored all six assets.

**Basis:** Summary and filter behavior observed; independent incoming-person comprehension SC-005 remains unvalidated.

**Checks:** UI-12; UI-16; UI-20–22; UI-30; UI-32/33; existing REQ-04/05 test; source inspection. **Findings:** Validation remaining: SC-005.

### REQ-06 — Energy-source locks and documented release gate

No unrelated field blocks lock capture; active lock blocks production/release; Technician release is refused; cross-person removal and supervisor authorization are stamped. A removed lock that was never verified still permits release, and earlier production timestamps remain possible.

**Basis:** Written role and applied-lock guards work; the selected hazardous-energy goal is only partly supported by the current completeness and chronology rules (F-01/F-02).

**Checks:** UI-01; UI-03–08; UI-20; existing REQ-06 tests; PROBE-01/02/06. **Findings:** F-01; F-02.

### REQ-07 — Incoming-shift acknowledgment and deadline

06:29 is Awaiting acknowledgment; 06:30 is Not acknowledged; verified active-lock acknowledgment records incoming user and applier; Operator role is refused. A current-shift note changes an overdue handover to Current shift with no acknowledgment.

**Basis:** Nominal boundaries/roles work; explicit acknowledgment obligation is ambiguous after current-shift edits (F-04).

**Checks:** UI-20–24; existing REQ-07/09 tests; PROBE-04. **Findings:** F-04.

### REQ-08 — Next-full-shift verification and repeat links

06:10 first good part waits until 22:00; a late-coded matching pre-deadline stop reopens/links the repair. Reclassifying the ongoing stop as a different category yields Verified – ran full Swing shift despite no subsequent first good part.

**Basis:** Literal same-reason/time algorithm behaves as specified, but it cannot establish the claimed full-shift operation or durable fix (F-05).

**Checks:** UI-25–30; existing REQ-08 tests; PROBE-05. **Findings:** F-05.

### REQ-09 — Prevent incomplete-lockout closure and handover

Unverified active lock blocks handover and names the source; verified active lock can be handed over; closure waits for removed locks and release. Once an unverified lock is removed, its missing verification is no longer a gate.

**Basis:** FR-020(a)/(b) work as narrowly written; the broader complete-record goal excludes required historical fields from its closure check (F-01).

**Checks:** UI-02; UI-06–08; UI-20; existing REQ-06/09 and REQ-09 tests; PROBE-01. **Findings:** F-01.

## Limits on satisfaction claims

Thirty-three browser observations are preserved: 32 completed UI observations, including successful and problematic paths, plus one photo-upload attempt blocked by browser-extension file access. The 15 existing domain tests passed. Six additional probes reproduce the findings; their successful assertions mean the problematic behavior was reproduced, not that the requirements passed. No student or stakeholder usability session is represented by these automated/browser-agent checks.

SC-004 and SC-005 require real participant timing/comprehension checks. The browser photo-upload/display path remains unverified because the file chooser could not receive the synthetic fixture without extension file-URL permission. The Open repairs/All machines filter passed UI-32/33. Photo-only domain state and summary behavior were exercised by the existing tests.

No authenticated production system, physical machine control, real sensor, persistence, offline operation or full audit trail was tested or claimed. Those declared prototype exclusions are not automatically classified as V1 implementation defects.

Application source was not changed. The browser demo was reset after testing. Specification changes proposed in findings.md must be reviewed before implementing V2.
