# Learning Log – 17-626 HW3 Spec-Driven Development

**Team:** Timothy Zhang, Carl Patel, Austin Huang  
**Repo:** https://github.com/CarlPatel/HW3-Spec-Driven-Development  
**V1:** https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v1  
**V2:** https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v2  

Traceability Matrix Links:  
V1: https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/v2/traceability.md  
V2: https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/v2/docs/traceability-v2.md  


---

## 1. Sprint Planning and Requirements Selection

### Scope and why

We merged the three teammates' goal models (`docs/goal-model.md`) and rated each goal as core, user-facing or uncertain. We selected the goals below and deferred the rest.

| Selected goal | REQ | Why selected |
|---|---|---|
| G1.1 Complete downtime event tied to a machine (incl. G1.1.1 sensor stop, G1.1.2 manual stop, G1.1.3 stop-to-good-part duration) | REQ-01, REQ-02 | Core: Angela's "one feature first" (T2-L80). Uncertain: sensor vs. sensorless presses (T1-L92). |
| G1.2 Close only with reason code and times (G1.2.1 quick reason list) | REQ-03 | Core and user-facing. Directly conflicts with the low-effort goal G4, so it is a good test of conflict handling. |
| G1.3 Repair not restarted after shift change (G1.3.1 record, G1.3.2 show at press, G1.3.5 incoming-shift acknowledgment) | REQ-04 (G1.3.1), REQ-05 (G1.3.2), REQ-07 (G1.3.5) | Named in all three teammates' models. Uncertain: verbal handover vs. written record. |
| G1.9 Next-full-shift repair verification | REQ-08 | Added to cover Teo's definition of "done" (T1-L90), which conflicts with Angela's (first good part). |
| G2.1 / G2.1.1 Hazardous energy: LOTO recorded, release gated by supervisor | REQ-06 | Rob's top priority. Uncertain: uptime vs. safety, and who authorizes release. |
| G3.4 Incomplete LOTO record blocks closure/handover | REQ-09 | Turns Rob's audit concern into a testable gate. |
| G4 (G4.1, G4.3, G4.4) Low entry effort, as a constraint | Constraint on REQ-01, REQ-04, REQ-06 | Quality goal shaping every selected goal: no required field may block opening an event or starting isolation. |

### What we deferred (and why)

| Deferred goal | Reason |
|---|---|
| G1.4 Early warning / press quirks | Needs real sensor trends; unresolved ownership of technicians' personal notes (conflict R13). |
| G1.5 / G2.2 Alerts and alert routing | Needs live sensors; alert-suppression vs. safety-alert conflict (C-3) preserved. |
| G1.6 MTBF, G1.7 PM planning | Depend on G1.1 data existing first. |
| G1.8 Spare-part bin location | Not tied to any conflict; lower learning value. |
| G2.3 Near miss / spill reporting | Separate workflow from repair; a V2 candidate. |
| G3.2 / G3.3 Audit history and retrieval | Partly met by auto-stamping in REQ-04/06. |
| G4.2 Voice note, G4.5 Nickname search | Noisy-floor feasibility risk (I-4); short mock list. |
| G5 Offline, G6 Distraction | No backend, so G5 deferred (conflict C-5 kept); G6 used only as a design constraint on REQ-06. |

### Overlaps, dependencies and conflicts, and decisions

The goal model showed these relationships before we wrote any spec text.

| # | Relationship | Decision | Why |
|---|---|---|---|
| R1 | Overlap: REQ-04 writes / REQ-05 shows the open-repair record | One data record, two requirements | Writing and viewing are tested separately. |
| R2 | Overlap: REQ-01 / REQ-02 both under G1.1 | Implement separately on one event | Opening and measuring are different user actions. |
| O-3 | Overlap: REQ-06 release gate / REQ-09 incomplete-lockout gate | Combine the gate, keep two requirements | REQ-09 extends the same check to closing and handover. It traces to Rob's records goal (G3.4); REQ-06 traces to his energy-control goal (G2.1). |
| R3–R5 | Dependencies: everything needs an open event (REQ-01); REQ-05 needs REQ-04; REQ-07 needs REQ-05; REQ-08 needs REQ-03; REQ-03 → REQ-02 → REQ-06 | Build and test in dependency order | A locked-out press cannot produce, so first good part can only be confirmed after release (T3-L12). |
| R6 | Conflict C-1: required reason code (REQ-03) vs. minimal effort (G4) | Compromise: required only at closure, from a short list | Angela states both needs herself (T2-L16). |
| R7 | Conflict C-4: coded field vs. free note/photo | Combine: code required; note/photo add detail but never replace it | T2-L9 "not just free-text"; T1-L95 "neat boxes". |
| R8 | Conflict C-2: downtime vs. safety hold | **Safety wins.** Release gate cannot be bypassed. Whether LOTO hold time counts as downtime is **unresolved**; V1 uses one clock and flags "included LOTO hold" | Needs Angela and Rob together. Preserved, not removed. |
| R9 | Conflict C-6: full LOTO detail vs. no distraction | Compromise: one tap per energy source, auto-stamped | T3-L50, T3-L27. |
| R10 | Inconsistency I-2: "done" = first good part (Angela) vs. "ran a full shift without me" (Teo) | Implement both: first good part ends downtime (REQ-02); next-full-shift verification added (REQ-08) | Closing an event does not mean the fix is verified. |
| R11 | Inconsistency I-3: face-to-face handover vs. system record | Keep both; add incoming-shift acknowledgment (REQ-07) | Face-to-face stays a human step; system holds the auditable record. |
| R12 | Who authorizes release? | Shift supervisor | Rob (T11-L14) and Angela (T5-L76, T10-L24) agree. |

**How the goal model helped.** 

The conflicts are structurally visible when every requirement is put under a goal with an owner. For example, REQ-03 (Angela, G1.2) and G4.3 (Teo and Angela) sit under the same parent, G1, so the C-1 conflict is within one stakeholder's own goals rather than between people. This suggests a compromise of requiring code only at closure was the right approach. In contrast, C-2 sits between two top-level goals owned by different people (G1 Angela, G2 Rob), so no single stakeholder could settle it. That is why we left it open.

### Judgment calls

**Why safety outranks downtime in R8, even though Angela's goal is downtime.** The two goals fail differently: a wrong downtime figure can be corrected later, but an injury cannot be undone. The gate also costs Angela little, because her lost time comes from missing records (T2-L40), not from lockouts.

**Why we added REQ-07 to REQ-09 to the original six.** See "Scope and why" above. In short, the original six avoided the uncertain parts of the model, and the added three cost little because they reuse the same event.

**Why I-2 was implemented as both instead of choosing one.** Angela and Teo describe two different moments, not competing definitions: production resuming, and the repair holding. Choosing Angela's would miss repeat faults; choosing Teo's would keep downtime running for up to a shift. F-05 later showed that our version of Teo's milestone was too weak, not that keeping both was wrong.



---
## 2. Prototype Evaluation
Here we compare our generated V1 website with our specification and the stakeholder goals at the time. All 15 existing domain tests passed, and six additional probes reproduced five issues identified during evaluation. Human entry-time and handover-comprehension checks remained pending, and browser photo selection was blocked. For each of the nine selected requirements, the traceability matrix records the interview evidence, goal ID, implemented behavior or code, and satisfaction status. All five of our findings below were classified as requirements issues because the written rules allowed behavior that didn’t really align with a stakeholder goal.

**F-01 · Incomplete isolation evidence (REQ-06, REQ-09)**. On Molder 8, V1 allowed release and closeout after an electrical lock was removed without a recorded zero-energy verification. Later we found that a separate probe showed that a listed energy source could be omitted without recording whether it applied to the job. FR-020 checked verification on active locks at handover, leaving a gap once a lock was removed. The stakeholder goal of a complete isolation record requires retained verification evidence and an explicit decision about each source’s applicability.

**F-02 · Inconsistent production timestamps (REQ-02, REQ-06)**. After the electrical lock was removed and release was recorded at 14:00, V1 accepted 12:00 as the “first good time” and reported 415 minutes of downtime. FR-005 checked the timestamp against the stop, while FR-015 checked whether the operator was currently allowed to confirm production. Together, those rules left the entered time unchecked against the release record. Accurate downtime reporting requires the “first good part time” to be at or after recorded removal and release.

**F-03 · A second stop was lost during pending closeout (REQ-01, REQ-02, REQ-08)**. Press 17 stopped at 06:55, resumed at 07:10, and stopped again at 07:25 while the first event’s paperwork was pending. V1 reused the first record and kept downtime frozen at 15 minutes. FR-003 deduplicated stops while an event was open, and the interviews allowed reason codes to be entered later. To preserve accurate breakdown and recurrence records, the spec needed to distinguish an active downtime interval from an event awaiting paperwork.

**F-04 · A note cleared an unacknowledged handover (REQ-07)**. We also found that saving a note in the current shift removed the overdue indicator and acknowledgment button even though the acknowledgment count remained zero. FR-016 used the latest work time to determine handover eligibility, while FR-017 set a deadline for unacknowledged events. This inconsistency made it murky regarding whether the incoming shift had accepted responsibility. The spec needed to keep the obligation visible until the incoming shift explicitly acknowledged it.

**F-05 · Repair verification lacked evidence of operation (REQ-08)**. V1 marked a hydraulic repair as verified for a full shift after a later stop was coded Electrical/Heater, even though the machine remained stopped throughout that shift. FR-018 and FR-019 used a matching reason code to detect recurrence. The stakeholder goal of verifying the repair required evidence of a full operating shift. The spec needed to define what evidence establishes continuous operation and how to handle stops whose reason is still unknown.


---

## 3. Revisions and Learning

For V2, we revised the goal model and spec first (new spec 003, commit `2177b9f`) and changed the code only after that (`d072b14`). V2 adds no features: REQ-01 to REQ-09 remain, and the new functional requirements FR-021 to FR-027 replace the V1 clauses that caused the findings.

### Change 1 — F-03: separate "currently stopped" from "waiting for paperwork"

| Item | Content |
|---|---|
| What we initially intended | FR-003 (REQ-01): one open event per machine. A second stop signal while an event is open reuses that event, so a sensor that fires twice does not create duplicates. |
| What evaluation showed | UI-19 / PROBE-03. Press 17 resumed at 07:10 with its reason code and closure still pending. A real new breakdown at 07:25 was merged into the old event. No new interval was created, so the second stop was never recorded. The spec used "open" for two different things: the machine is stopped, and the record is not yet closed. |
| What we changed and why | **Goal model:** G1.1 / G1.1.1 / G1.1.3 refined into one *active stop interval* per machine plus separate *pending closeout* records. **Spec:** FR-024. An active stop is defined by the absence of a first good part. Signals during it are still deduplicated. After first good part, a new stop always creates a new interval linked to its predecessor, even if older records still need a reason or closure. **Prototype:** a "Pending closeout" panel and links from each new stop to the previous one. |
| How V2 better serves the goal | Angela's downtime data no longer depends on how quickly someone finishes paperwork. Late coding cannot hide a breakdown. Acceptance scenario 4 and the domain test "new stop after good part is captured while reason/closure remain pending" both pass: the first record keeps its 15 minutes, the new stop runs separately, and closing the old record leaves the new one active. Duplicate sensor signals are still merged, so the original purpose of FR-003 is kept. |

### Change 2 — F-02: production time must follow the release record

| Item | Content |
|---|---|
| What we initially intended | FR-005: first good part must be after the stop and not in the future. FR-015: first good part cannot be *entered* while locks are applied or release is missing. |
| What evaluation showed | UI-07/08, PROBE-02. With a lock from 06:10 to 14:00 and release at 14:00, a first good part of 12:00 was accepted, and the event closed showing 415 minutes. Each rule checked the *current* state at the moment of entry. None checked that the *times* in the record were in a possible order. |
| What we changed and why | **Goal model:** for G2.1 / G2.1.1, chronology became part of a complete record, not just a matter of current permission. **Spec:** FR-023 requires stop ≤ apply ≤ verify ≤ remove ≤ release ≤ first good part (equal times allowed). First good part may not fall inside any isolation interval, and a new lock invalidates an earlier release. |
| How V2 better serves the goal | The record can no longer claim a press produced parts while it was locked out. That protects both Rob's release record and Angela's downtime minutes. In the browser check, 06:50 production after a 07:40 release is refused with an explanation, and 14:00 after a 14:00 release is accepted. A relock test confirms each cycle needs its own verification and that release must be re-authorized. |

### Change 3 — F-01: isolation evidence is checked for the whole history, not just current locks

| Item | Content |
|---|---|
| What we initially intended | FR-020 (REQ-09) and FR-012–015 (REQ-06): block closure while any lock is applied, and block handover while any *applied* lock lacks zero-energy verification. |
| What evaluation showed | UI-02/06, PROBE-01. An Electrical lock applied without verification and then removed no longer counted. Supervisor release and closure both succeeded, so the record showed a complete lockout that never verified zero energy. A source that was never locked at all was also not flagged. The rule protected the *present* while Rob's goal concerns the *history*. |
| What we changed and why | **Goal model:** G2.1 / G2.1.1 / G3.4. Complete evidence means every applicable energy source and every lock cycle's verification and removal. **Spec:** FR-021: once LOTO is used, every source of the machine is *applicable* by default. Only a shift supervisor may mark a source not applicable, and must give a reason, which is stamped and kept in the timeline. A source with any recorded lock cannot be excluded. FR-022: release and closure list every missing item even after removal, including missing verification, verifier, applier, remover and bad chronology. Removal without verification can still be *recorded*, because that is what happened, but it stays an incomplete record. **No backfill:** V2 does not let anyone add a verification after the fact. **Prototype:** a supervisor-only source applicability form and a "Release / closeout checks" list of missing items. |
| How V2 better serves the goal | A missing verification cannot disappear by removing the lock, and a forgotten energy source is now visible. Handover still works with *verified* active locks, because the outgoing technician should not have to remove locks just to hand over. Four F-01 domain tests pass, and a technician's attempt to exclude a source is refused. We deliberately chose to leave an unverified removed lock as a permanent gap rather than allow a retrospective correction. A correction feature would need Rob to define who may correct a safety record and how (G3.2, no silent overwrite), and that is outside this sprint. |

### Change 4 — F-04: acknowledgment is an explicit act, not a side effect of editing

| Item | Content |
|---|---|
| What we initially intended | FR-016: a handover is owed when the event's *latest entry or lock* is from a previous shift. FR-017: it is overdue 30 minutes into the shift. |
| What evaluation showed | UI-24, PROBE-04. At 06:30 Molder 8 showed "Not acknowledged." Saving any note during the current shift made the latest entry "current," and the status changed to "Current shift" with zero acknowledgments. Writing a note silently counted as accepting responsibility. |
| What we changed and why | **Goal model:** G1.3.5 is an explicit obligation per dated shift, separate from adding work notes. **Spec:** FR-025. An unclosed event that started before the current shift owes one explicit acknowledgment for that shift. Notes, removal, verification and reason edits never clear it. Operators still cannot acknowledge. A change to critical isolation information after acknowledgment (a lock applied, verified or removed, or a source decision) requires a new acknowledgment. The earlier acknowledgment is kept as a snapshot. |
| How V2 better serves the goal | Rob's request that the incoming shift explicitly takes over (T11-L22) is now enforced. In the browser, a current-shift note leaves the handover "Not acknowledged"; only the acknowledge action clears it, and the next shift owes its own. If someone changes the lockout after acknowledgment, the incoming person has to look at it again. |

### Change 5 — F-05: "verified" requires evidence of a full operating shift

| Item | Content |
|---|---|
| What we initially intended | FR-018/019 (REQ-08): a closed repair becomes Verified at the end of the next full shift if no new event *with the same reason code* opens on that machine; a same-code event reopens it. |
| What evaluation showed | UI-25–30, PROBE-05. A repair showed "Verified – ran full Swing shift" while the machine was recorded as stopped all shift, because the later stop had a different reason code. Our rule treated "no matching code" as proof that the machine ran, which is not what Teo meant by "ran a full shift without me" (T1-L90). |
| What we changed and why | **Goal model:** G1.9. Absence of a matching category is weaker evidence than a recorded full operating shift; verification depends on production intervals and every stop in between. **Spec:** FR-026: Verified only when recorded operation covers an entire shift after first good part with no new stop. A stop with a different code interrupts the evidence, so the system waits for production to resume and then for the next complete shift. FR-027: a same-code stop before that reopens the repair. An *unknown* reason keeps it "Awaiting evidence." Statuses now distinguish Awaiting closeout, Awaiting evidence, "No matching recurrence observed — awaiting a full operating shift," Reopened, and Verified. **Prototype:** the new statuses and the operating evidence behind them are shown on each repair. |
| How V2 better serves the goal | "Verified" now means what Teo said it means. In acceptance scenario 6, an unrelated stop at 07:00 with no later good part no longer yields Verified at 22:05. If production resumes at 15:00, the Night shift can qualify at 06:00 the next day. Six F-05 domain tests pass, including the exact-boundary cases. **Limit kept explicit:** matching by reason code is still only a proxy for "the same fault." We did not claim to solve fault identity. |

### Goal-model changes

The V2 section of `docs/goal-model.md` refines four existing goals and keeps their IDs, owners and evidence. No goals were added or removed. The V1 model is frozen in `versions/v1/goal-model.md`.

| Goal | V1 meaning | V2 meaning |
|---|---|---|
| G1.1 / G1.1.1 / G1.1.3 | One open event per machine | One *active stop interval* per machine, plus separate *pending closeout* records |
| G2.1 / G2.1.1 / G3.4 | Currently applied locks are complete and verified | All applicable sources, every historical lock cycle, and a valid chronology |
| G1.3.5 | Acknowledgment owed when latest activity is from a previous shift | Explicit per-shift obligation, separate from authorship; critical changes need re-acceptance |
| G1.9 | No same-code repeat by end of next shift | A recorded, uninterrupted full operating shift |

The conflicts are preserved: C-1, C-4 and C-6 are unchanged, C-2 (whether LOTO hold counts as downtime) is still unresolved, and I-2 and I-3 were tightened by F-05 and F-04.

### Reflection

**1. Which decisions required our judgment rather than relying solely on AI?**
The AI could generate specs, code and even an evaluation, but several decisions could not be delegated. When selecting and building the spec sheet, the agent oversimplified the problem by limiting the scope. At the start, the agent limited the spec requirement to only 6, requiring us to correct the scope to spec 002. We also need to make explicit prioritization choices for certain goals, such as prioritizing safety over downtime. We also need to accept and challenge the five findings labeled in the evaluation based on our own call. We also need to choose the policy defaults for V2 by weighing the benefits and cost, such as refusing to backfill verification on a removed lock due to the large amount of cost incurred on Rob despite making tests easier to pass.


**2. How did prototyping change our understanding of stakeholder needs?**
Prototyping allowed us to clearly understand and visualize the conflicts between stakeholders that aren’t directly visible from the spec sheet. Using the prototype showed that Rob's goal is about a complete, ordered history, not a gate on the present (F-01, F-02). It showed that Angela's downtime figure is only as good as the event lifecycle behind it (F-03), and that Teo's "ran a full shift" is a claim that needs evidence (F-05). We also learned that each of us interpret "open" and "acknowledged" differently, and prototyping allows us to come together with a more consistent idea.

**3. How did spec-driven development help maintain consistency?**
Spec-driven development allows us to test and verify our changes through all the key requirements throughout development. When we revised the spec, the V2 traceability matrix could show exactly which functions changed for which finding. Writing the 003 spec before touching code also kept V2 scoped. Because of this, V2 included only revised meanings for existing requirements, and the constitution blocked scope creep. Having the spec available allows all of our changes to stay consistent with the specifications from the stakeholders.

**4. What evidence would we present to management?**
Despite all tests passing for V1, 8 of the 9 requirements were only partially satisfied. Their gaps are identified through human-directed evaluation. V2 addressed five specification gaps in the mock prototype. Two of them (F-01 verification history, F-02 release chronology) would have let the record show a complete, released lockout that never verified zero energy or that "produced" while locked out. All of the changes are consistent with the specs and are traceable, with each V2 code change tracing through FR-021 to FR-027 to a finding, a goal, and an interview line. V1 is also preserved for comparison and references. The existing conflicts are reasoned but not deleted simply because removing them would optimize for a passing spec. C-2 still openly unresolved, and I-2 kept as two milestones. 

