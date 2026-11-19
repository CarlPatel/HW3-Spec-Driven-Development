# Learning Log – 17-626 HW3 Spec-Driven Development

**Team:** Timothy Zhang, Carl Patel, Austin Huang  
**Repo:** https://github.com/CarlPatel/HW3-Spec-Driven-Development  
**V1:** https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v1  
**V2:** https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v2  

Traceability Matrix Links:  
V1: https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/v2/traceability.md  
V2: https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/v2/docs/traceability-v2.md  



## 1. Sprint Planning and Requirements Selection

### Scope and why

We merged the three teammates' goal models (`docs/goal-model.md`) and rated each goal as core, user-facing or uncertain. We selected the goals below and deferred the rest.

The first core goal is downtime per machine, which is Anegla’s first priority. They can be accessed through sensors or manually and are closed with a code reason.

The second core goal is breaking down shift handover, a core component mentioned by all models, into three requirements: record the repair's progress, show it at the press, and have the incoming shift acknowledge it .

The third core goal is Rob's lockout safety, his top priority. Before working on a press, a technician locks out each energy source, and the press can return to production only after every lock is removed and a shift supervisor approves the release. An incomplete lockout record cannot be closed or handed to the next shift.

We also selected repair verification, which is user-facing and uncertain rather than core. Angela considers a repair done at the first good part, while Teo considers it done only after the machine runs a full shift without him, so the system waits a full shift before marking a repair verified.

Finally, low entry effort is a constraint on every goal rather than a feature: no required field may stop someone from reporting a breakdown or making a machine safe.



We also chose to defer several goals since they are not possible at the current stage. Alerts and early warning need real sensors, which a mock prototype does not have. Failure statistics and maintenance planning need downtime data to exist first. Near-miss reporting is a separate workflow from repairs, and voice notes are impractical on a noisy shop floor.

The goal model also showed how the selected goals relate. Recording a repair's progress and showing it at the press use the same record. However, we kept them as separate requirements because writing and viewing are tested differently. Every requirement depends on a downtime event existing first, and the first good part can only be recorded after the lockout is released since a locked press cannot produce.

We have also identified conflicts within the goals of each candidate. The first conflict is within Angela's own goals: she wants a required reason code but also minimal effort for technicians. We compromised by asking for the code only when the event is closed.

The second conflict is between Angela's downtime goal and Rob's safety hold. We prioritized safety, because a wrong downtime figure can be corrected but an injury cannot. We left open whether lockout time counts as downtime, since only Angela and Rob together can decide that.
The third conflict is over when a repair is done. Angela's answer, the first good part, and Teo's, a full shift without problems, describe different moments, so we kept both.

**How the goal model helped.** 

The conflicts became visible once every requirement was placed under a goal with a named owner. For example, the required reason code at closure and the rule that no required field may block a technician during a breakdown both fall under Angela's goal of reducing downtime. Since the reason code is required only when the event is closed, this suggests to us that a compromise is the best choice here. In contrast, the conflict between downtime and safety hold sits between two top-level goals owned by different people: Angela's goal of reducing downtime and Rob's goal of avoiding injury. No single stakeholder could settle it, so we left it open. 

### Judgment calls

When Rob’s safety goal conflicts with Angela’s downtime prevention goal, we decide that safety outranks downtime due to a safety concern being far less recoverable than lost production. 
When there are two conflicting definitions of a finished repair from Angela and Teo, we chose to implement both definitions instead of choosing one. This is due to the scenarios the two stakeholders are describing - production resuming and repair holding - are very different and should be evaluated differently.


## 2. Prototype Evaluation

We evaluated the V1 prototype against our specification and the stakeholder goals. All 15 existing tests passed, and six additional probes reproduced five issues found during evaluation. The checks with real people (entry time and handover comprehension) were not run, and the browser photo upload could not be tested. The traceability matrix links each of the nine requirements to interview evidence, a goal, the implemented behavior and a satisfaction status. We classified all five findings as requirements issues: in each case V1 followed the written rules, but those rules allowed behavior that did not serve a stakeholder goal.

**Incomplete isolation evidence**. V1 allowed release and closeout after an electrical lock was removed without any recorded zero-energy verification. It also allowed one of a machine's energy sources to be skipped without recording whether that source applied to the job. The rule checked verification only on locks still in place. A complete isolation record needs verification evidence that survives removal, and an explicit decision about each energy source.

**Inconsistent production times**. With release recorded at 14:00, V1 accepted 12:00 as the first good part time and reported 415 minutes of downtime. One rule checked the time against the stop, and another checked only whether production could be confirmed at that moment. Neither compared the entered time with the release record. Accurate records require the first good part to come at or after removal and release.

**Second stop lost during pending paperwork**. Press 17 stopped at 06:55, resumed at 07:10, and stopped again at 07:25 while the first event's paperwork was still pending. V1 reused the first record, and downtime stayed frozen at 15 minutes. The spec treated an "open" event as a stopped machine, even though stakeholders allow reason codes to be entered later. It needed to separate an active stop from an event awaiting paperwork.

**A note cleared an unacknowledged handover**. Saving an ordinary note during the current shift removed the overdue warning and the acknowledgment button, even though nobody had acknowledged the handover. Two rules conflict on how handover is handled: one based handover on the latest work entry, and another set a deadline for acknowledgment. The obligation needed to stay visible until the incoming shift explicitly acknowledged it.

**Verification without evidence of operation**. V1 marked a hydraulic repair as verified for a full shift after a later stop was coded as electrical, even though the machine stayed stopped the whole shift. Only a matching reason code counted as a repeat fault. Verifying a repair requires evidence of a full operating shift, including rules for stops whose reason is not yet known.



## 3. Revisions and Learning

When updating the goal model and changing to a new spec, we target our changes to make the existing rules even stricter.

The first change separates a stopped machine from unfinished paperwork. We originally allowed one open event per machine so that a repeated sensor signal would not create duplicates. Testing showed that a new breakdown was swallowed by the old event while its paperwork was pending. V2 tracks the current stop separately from records awaiting closure, so late paperwork can no longer hide downtime.

The second change enforces the order of events. We originally only blocked production while a lock was on. Testing showed that a production time earlier than the lockout release was accepted. V2 requires stop, lock, verification, removal, release and first good part in that order, so the record cannot claim the press produced parts while locked.

The third change checks the whole lockout history. We originally checked only locks that were still on. Testing showed that removing an unverified lock erased the gap. V2 requires evidence for every energy source and every lock, even after removal, and only a supervisor may exclude a source, with a reason. We chose not to allow verification to be added afterwards, so gaps stay visible to Rob.

The fourth change makes handover acceptance explicit. We originally treated a handover as owed only when the latest entry came from a previous shift. Testing showed that writing a note silently cleared an overdue handover. V2 requires the incoming shift to acknowledge every handover, and notes cannot clear it.

The fifth change tightens repair verification. We originally treated the absence of a repeat with the same reason code as proof that the repair held. Testing showed a repair marked verified while the machine sat stopped all shift. V2 requires a full shift of recorded operation, matching what Teo meant.


### Reflection

**1. Which decisions required our judgment rather than relying solely on AI?**

While we were building the specification, the agent worked from an earlier six-requirement draft instead of the expanded nine-requirement scope, and we had to correct it. We also had to make explicit prioritization choices, such as putting safety ahead of downtime. We had to decide for ourselves whether to accept or challenge how the evaluation classified its five findings. Finally, we chose the policy defaults for V2 by weighing benefits against costs. For example, we refused to let verification be added after a lock was removed: that option would have made the tests easier to pass, but it would have weakened Rob's safety record. 


**2. How did prototyping change our understanding of stakeholder needs?**

Prototyping exposed gaps that were not visible from reading the specification. Using the prototype showed that Rob's goal is about a complete, ordered history, not just a check on the machine's current state. It also showed that the reliability of Angela's downtime figure is heavily tied to the robustness of the related event records. We also learned that terms like "open" and "acknowledged" each carried two meanings in our specification, and the prototype forced us to resolve them by either splitting them up or agree on one meaning.

**3. How did spec-driven development help maintain consistency?**

Spec-driven development lets us check every change against the key requirements throughout development. When we revised the specification, the updated traceability matrix showed exactly which parts of the code changed for which finding. Writing the revised specification before touching the code also kept V2 in scope by changing the meaning of existing requirements without adding new features. Since every requirement traces back to stakeholder interviews, our changes stayed consistent with what the stakeholders asked for. 

**4. What evidence would we present to management?**

Although all 15 AI-generated tests passed for V1, 8 of the 9 requirements were only partially satisfied. Human-directed evaluation found those gaps. V2 addressed five specification gaps in the mock prototype. Two of them would have let the record show a completed, released lockout that never verified zero energy, or a press that "produced" parts while it was still locked out. Every V2 change is traceable from a finding to a revised requirement, a goal and an interview line, and V1 is preserved for comparison. We also kept the stakeholder conflicts and documented our reasoning rather than deleting them instead of deleting them to improve spec validity. The conflict over whether lockout time counts as downtime remains open, so both definitions of a finished repair are kept. 
