# Step 4 — Evaluation findings and V2 candidates

Baseline: [V1 `bef8e6c`](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/bef8e6c0bfae46af486e561841c32f9c8d159b88), authoritative 002 spec. Evaluated November 15, 2026.

These are technical observations and proposed requirement changes. They are not a student learning log, personal reflection or stakeholder approval. No V2 change has been implemented.

**Classification:** The five significant observations below are requirements omissions or inconsistencies exposed by the prototype. The existing implementation follows the relevant narrow rules in these paths; there is no confirmed unambiguous application-code defect among these five findings. Implementing a V2 change should follow an explicit spec/model revision. Lesser unverified coverage is listed separately.

| ID | Priority | Finding | Requirements | Classification |
|---|---|---|---|---|
| F-01 | High | Removed locks can hide missing verification and source applicability | REQ-06, REQ-09 | Requirements issue |
| F-02 | High | Production timestamps can contradict the recorded release chronology | REQ-02, REQ-06 | Requirements issue |
| F-03 | High | A new breakdown disappears while an earlier event awaits paperwork closure | REQ-01, REQ-02, REQ-08 | Requirements issue |
| F-04 | Medium | A current-shift note clears the overdue handover obligation | REQ-07 | Requirements issue |
| F-05 | Medium | No matching reason code is treated as proof that the machine ran a full shift | REQ-08 | Requirements issue |

## F-01 — Removed locks can hide missing verification and source applicability

**Priority:** High. **Goals:** G2.1, G2.1.1, G3.4. **Evidence:** T3-L14 T6-L64 T6-L81 T6-L98 T6-L111.

**Observed:** Molder 8: apply an Electrical lock without zero-energy verification, remove it, authorize release as Alex, and close the event. All actions are accepted. A separate domain probe records only Hydraulic on a machine whose listed energy sources are Hydraulic and Electrical; acknowledgment and release do not require a job-level decision on the other source.

**What it reveals:** The selected goal concerns complete isolation evidence. The current gates inspect active/applied locks, not historical required verification or an explicit set of task-applicable sources. This can produce a complete-looking closed record with an unverified isolation. A source listed on a machine is not automatically applicable to every task; that applicability must be explicit rather than guessed.

**Classification:** Requirements issue: FR-020(a) requires removed locks and authorization, while (b) checks zero energy only on currently applied locks at handover. The implementation follows that narrow rule. The broader selected completeness goal is not fully translated into the rule.

**Proposed specification change:** Define task-applicable energy sources and required isolation evidence. Require retained verifier identity/time and all applicable completion fields at release/closeout, even after removal. Show each missing field. Keep active-isolation handover distinct from eventual release; do not demand lock removal merely to hand over.

**Acceptance check after revision:** Remove an unverified lock and attempt release/closure: missing verification must be listed. Omit an applicable source: a missing-source decision must be listed. Valid verified active isolation must still support the documented handover path.

**Clarification:** Rob and the team must confirm task applicability, required lifecycle fields and who may verify/remove/release. The prototype does not establish a real-world isolation policy.

**Reproduction evidence:** UI-01/02/06/08; PROBE-01/06. [Relevant source](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L49).

## F-02 — Production timestamps can contradict the recorded release chronology

**Priority:** High. **Goals:** G1.1.3, G2.1.1. **Evidence:** T2-L9 T2-L14 T11-L14 T11-L22.

**Observed:** On the live demo, an Electrical lock is recorded from 06:10 until 14:00 and release is recorded at 14:00. The Operator can then submit first good part at 12:00. The event closes and displays 415 downtime minutes from its 05:05 stop, even though 12:00 falls within the recorded lock interval.

**What it reveals:** The action happens after release, but its stored event time says production resumed before release. The duration arithmetic is correct for its inputs; those inputs are inconsistent with the safety record.

**Classification:** Requirements issue: FR-005 constrains time relative to stop, and FR-015 constrains the current permission to confirm. Neither explicitly constrains the entered historical production time relative to release or recorded isolation intervals. Do not label the missing temporal rule a proven violation of an unambiguous coded requirement.

**Proposed specification change:** Specify chronology invariants for stop, isolation, removal, authorization and first good part. For a LOTO event, reject production times earlier than the valid release or within an active isolation interval. If retrospective corrections are needed, define distinct event/recording times and a reviewed correction workflow.

**Acceptance check after revision:** After release at 14:00, first good part at 12:00 must be refused with a chronology message; a valid time at/after release succeeds. Existing earlier-than-stop and future-time tests must remain.

**Clarification:** Confirm with Angela and Rob whether retrospective production times and corrections are permitted and which timestamps are authoritative.

**Reproduction evidence:** UI-07/08; PROBE-02. [Relevant source](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L51).

## F-03 — A new breakdown disappears while an earlier event awaits paperwork closure

**Priority:** High. **Goals:** G1.1, G1.1.1, G1.1.3, G1.9. **Evidence:** T2-L14 T2-L16 T2-L63 T2-L80.

**Observed:** Press 17 stops at 06:55, first good part is confirmed at 07:10, and its reason/closure are left pending. At 07:25, Simulate another stop reselects the old r5 event. The stop remains 06:55, first good part remains 07:10 and downtime remains frozen at 15 minutes. No new stop interval is created.

**What it reveals:** The system treats unclosed paperwork as an ongoing stop even after production resumed. The interviews explicitly include reason codes entered later, so resumed production with incomplete paperwork is plausible. Accurate event and repeat-fault records cannot depend on instant administrative closure.

**Classification:** Requirements issue: FR-003 says one open event and US1-3 deduplicates another stop while it is open, but open is not separated from currently stopped. The implementation obeys that rule literally. It is insufficient for the machine-event goal after production resumes.

**Proposed specification change:** Separate the downtime interval from repair/work-order completion. Permit a fresh stop after a recorded first good part, even if earlier coding or closeout is pending. Define the invariant as one active stop interval per machine and deduplicate only signals within that same active interval. Preserve links to related repair work.

**Acceptance check after revision:** Resume at 07:10, leave the reason pending, and stop at 07:25: a fresh running interval must appear while the first interval retains 15 minutes. Repeated signals while the machine remains stopped must still deduplicate.

**Clarification:** Angela and Teo should confirm how stop intervals, work orders and recurrence relate when closure is delayed.

**Reproduction evidence:** UI-19; PROBE-03. [Relevant source](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L36).

## F-04 — A current-shift note clears the overdue handover obligation

**Priority:** Medium. **Goals:** G1.3.5. **Evidence:** T1-L47 T10-L11 T11-L22.

**Observed:** At 06:30 Molder 8 is Not acknowledged. Maya saves a normal finding without clicking Acknowledge handover. The view becomes Current shift, the acknowledgment button and overdue state disappear, and the acknowledgment count remains zero.

**What it reveals:** Entering work and accepting responsibility for the prior shift are different actions. The demo no longer exposes a missing explicit acknowledgment once someone edits the record.

**Classification:** Requirements issue / specification inconsistency: FR-016 and the clarification base eligibility on latest work time, while FR-017 describes a deadline for an unacknowledged event. The implementation follows latest-work eligibility. The team must decide whether a note is intended to count as implicit acceptance before treating this as a coding defect.

**Proposed specification change:** Define a pending handover per dated shift occurrence or responsibility transfer. Keep it pending until explicit authorized acknowledgment; ordinary entries must not erase it. Define whether changed critical isolation data after acknowledgment requires a new acknowledgment.

**Acceptance check after revision:** After the 06:30 deadline, save a current-shift note: the handover remains pending/highlighted with zero acknowledgments. Explicit acknowledgment records actor/time and clears the obligation.

**Clarification:** Confirm with Rob and Angela whether explicit acceptance is required and whether a Technician can satisfy the incoming-supervisor goal in this demo.

**Reproduction evidence:** UI-21/22/23/24; PROBE-04. [Relevant source](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L64).

## F-05 — No matching reason code is treated as proof that the machine ran a full shift

**Priority:** Medium. **Goals:** G1.9. **Evidence:** T1-L34 T1-L90 T9-L22.

**Observed:** A Hydraulic repair has first good part at 06:10 and its verification deadline is 22:00. The press stops again at 07:00 and never records another first good part. At 22:05, coding that ongoing stop Electrical/Heater makes the earlier repair say Verified – ran full Swing shift. The machine was recorded as stopped throughout that shift. The independent probe reproduces the same case for Day shift.

**What it reveals:** The code can establish absence of a same-category recorded repeat, not a full operating shift or successful verification cycle. A reason category is also a broad proxy for fault identity. These are different levels of evidence.

**Classification:** Requirements issue: FR-018/019 and the confirm-with-Teo assumption explicitly use same machine plus reason code. The implementation largely follows that algorithm; the criterion and display claim do not establish the stated stakeholder goal.

**Proposed specification change:** Distinguish Awaiting evidence, No matching recurrence observed and Verified repair. Define what counts as a full operating shift and require appropriate run/verification evidence, such as a recorded verification outcome or operating interval. Define a better fault identity or explicitly retain the limitations of category matching.

**Acceptance check after revision:** An unrelated stop covering the required shift must prevent a Ran full shift claim. A complete operating/verification interval can verify the repair; a matching fault reopens it; an uncoded stop keeps classification pending.

**Clarification:** Teo must confirm the verification horizon and evidence, and whether same reason code reliably identifies a repeat fault.

**Reproduction evidence:** UI-25–30; PROBE-05. [Relevant source](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/frontend/domain.js#L68).

## Coverage and scope limits

- Real participant entry timing (SC-004) and incoming-person comprehension/one-tap acceptance (SC-005) are pending. Browser-agent actions are not evidence of human usability.
- The browser photo flow was attempted with a synthetic fixture but blocked before file selection by extension file-URL access. No application upload result is claimed. Domain photo-only state passes the existing test. Open-only and all-machines filter interactions passed UI-32/33.
- FR-010 says verification state should appear in the machine view; closed records show it, while open records do not expose an explicit Not yet closed verification badge. Confirm whether an explicit open-state badge is required; no user-impact defect is asserted from the absent badge alone.
- Reload resets records, role switching is unauthenticated, and there is no real machine/sensor integration, offline sync or full audit history. These are declared V1 exclusions, not discoveries of unexpected production behavior.
- The prototype marks a reopened repair by linking a still-closed historical event to a new event. Confirm that this representation meets the team’s intended meaning of reopened; the observation is not separately counted as a defect.

## Reproduction

From this folder run `node reproduce-findings.mjs`. It loads the unchanged pinned domain module under `source-snapshot/` and asserts the observed behavior. Output is cached as `evidence/reproduction-probes.json`. These are six reproducibility probes, not six successful stakeholder acceptance tests.

Browser snapshots UI-01–UI-33 are in `evidence/`, together with screenshots of the release chronology, disappearing handover and verification label. The live demo was reset afterward.


## Captured screenshots

[Release chronology: production at 12:00, release at 14:00](evidence/UI-08-release-chronology.jpg)

[Overdue acknowledgment disappears after an ordinary note](evidence/UI-24-handover-disappears.jpg)

[Full-shift verification label on historical repair](evidence/UI-30-verification-evidence.jpg)
