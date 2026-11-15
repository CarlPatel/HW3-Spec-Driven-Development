# Merged Team Goal Model and Sprint Scope (V1)

System: tablet-based logging of equipment problems, repairs, and lockout/tagout for an
injection-molding plant (ABC Design Services client).

## 1. Sources

**Interview transcripts** (cited as `T#-L#`, where L is the CSV line number and the header is line 1)

| ID | Stakeholder | File | From |
|----|-------------|------|------|
| T1 | Teo Salinas, night-shift technician | `transcript-261026-2138.csv` | repo root |
| T2 | Angela Novak, plant manager | `transcript-261026-2218.csv` | repo root |
| T3 | Rob Kessler, EHS coordinator | `transcript-261026-2245.csv` | repo root |
| T4 | Teo | `Assignment 1/transcript-261028-1816 Teo.csv` | Carl zip |
| T5 | Angela | `Assignment 1/transcript-261028-1816 Angela.csv` | Carl zip |
| T6 | Rob | `Assignment 1/transcript-261028-1816 Rob.csv` | Carl zip |
| T7 / T8 / T9 | Teo (initial, follow-up 1, follow-up 2) | `stakeholder-interviews/teo-*.csv` | Teammate packet |
| T10 | Angela | `stakeholder-interviews/angela-initial.csv` | Teammate packet |
| T11 | Rob | `stakeholder-interviews/rob-interview.csv` | Teammate packet |

**Assignment 2 goal models** (cited as `M:`, `C:`, `P:` + the goal ID in that model)

| Prefix | Model | Location |
|--------|-------|----------|
| M | Teo / Angela / Rob / combined (G-1..G-115, conflicts C-1..C-6) | `Model/` |
| C | Carl: Teo / Angela / Rob / combined (G-1..G-132) | Carl zip, `Assignment 2/` |
| P | Timothy: Teo / Angela / Rob / combined (G-1..G-77) | Teammate packet, `assignment-2/` |

## 2. Merged goal model

The three teammate models agree closely. The merge keeps the most detailed version of each area
and renames goals to the hierarchical `G#.#` scheme. ★ marks a goal in sprint scope.
`(env)` marks a goal that people achieve outside the software.

```
G0  Safe, productive and auditable maintenance                      M:G-115
├─ G1  Reduce unplanned downtime on critical machines (Angela)      M:G-40  C:G-35  P:G-1
│  ├─ G1.1 ★ Complete downtime & repair event tied to the machine   M:G-41,G-46  C:G-39  P:G-30,G-33
│  ├─ G1.2 ★ Event closed only with reason code and times           M:G-47,G-54,G-55  C:G-40,G-82  P:G-31,G-32
│  ├─ G1.3 ★ Repair not restarted from scratch after shift change   M:G-45,G-4  C:G-24,G-44  P:G-6,G-14
│  │  ├─ G1.3.1 ★ Open-repair state recorded while open             M:G-65(+G-33)  C:G-7..G-12  P:G-9,G-10
│  │  ├─ G1.3.2 ★ Open-repair state & history shown at the press    M:G-10(+G-66)  C:G-3,G-4  P:G-15,G-27
│  │  └─ G1.3.3 (env) Face-to-face handover at the machine          M:G-29(+G-64)  P:G-29
│  ├─ G1.4  Catch failures before alarms / share press quirks       M:G-3,G-21,G-23  C:G-6,G-26  P:G-23
│  ├─ G1.5  Actionable alerts                                      M:G-68
│  ├─ G1.6  Root cause / MTBF by machine and failure mode          M:G-42,G-59  C:G-42,G-63
│  ├─ G1.7  PM findings and interval planning                      M:G-43,G-49  C:G-65..G-73
│  └─ G1.8  Spare-part bin location                                M:G-16  C:G-20  P:G-17,G-18
├─ G2  Avoid injury during maintenance (Rob)                        M:G-76  C:G-83  P:G-46
│  ├─ G2.1 ★ Hazardous energy controlled: LOTO recorded, release gated
│  │        M:G-78,G-81(+G-6),G-82,G-88,G-102  C:G-87,G-98,G-101,G-102  P:G-38,G-41,G-49,G-50
│  ├─ G2.2  Work stopped / unsafe-condition alert routing           M:G-79,G-89  C:G-125..G-128  P:G-69
│  └─ G2.3  Near miss within 24 h; separate spill report            M:G-99,G-100  C:G-106,G-112  P:G-62,G-66
├─ G3  Audit-ready maintenance & safety records (Rob, Angela)       M:G-77(+G-67)  C:G-84,G-56  P:G-40,G-56
│  ├─ G3.1  Who did what and when                                   M:G-48  C:G-57,G-120  P:G-55
│  ├─ G3.2  No silent overwrite of safety entries                   M:G-97  P:G-55
│  └─ G3.3  Complete machine record retrieved in < 1 min            M:G-58(+G-98)  P:G-56,G-58
└─ Soft / quality goals
   ├─ G4 ★ Minimize tablet entry effort during breakdown (Teo, Angela)  M:G-35(+G-72)  C:G-16,G-19  P:G-2
   │  ├─ G4.1 ★ Quick note or photo instead of long typing          M:G-36  C:G-12,G-13  P:G-11,G-12
   │  ├─ G4.2  Short voice note                                     C:G-14  P:G-13,G-72
   │  ├─ G4.3 ★ Required fields never block isolation               M:G-37
   │  ├─ G4.4 ★ Missing sensor data not treated as a fault          M:G-38,G-15  P:G-75
   │  └─ G4.5  Find press by floor nickname                         M:G-39  C:G-21,G-22
   ├─ G5  Records usable under poor connectivity                    M:G-50  C:G-119,G-132
   └─ G6  Minimize tablet distraction near moving equipment (Rob)   M:G-80  C:G-121  P:G-67,G-74
```

## 3. Sprint selection (Step 1)

Ratings: **Core** = without it the system has no purpose. **User-facing** = a stakeholder
touches it on the floor. **Uncertain** = stakeholders disagree or the evidence is incomplete.

| Goal | Core | User-facing | Uncertain | Decision |
|------|:----:|:-----------:|:---------:|----------|
| G1.1 Downtime event | ✔ (Angela's "one feature first", T2-L80) | ✔ | ✔ sensor vs. offline presses (T1-L92) | **Selected** |
| G1.2 Reason code at close | ✔ | ✔ | ✔ conflicts with G4 (C-1) | **Selected** |
| G1.3 Shift handover record | ✔ (named by all 3 models) | ✔ | ✔ verbal vs. record (I-3) | **Selected** |
| G2.1 LOTO + release gate | ✔ (Rob's top priority) | ✔ | ✔ uptime vs. safety (C-2); who authorizes release | **Selected** |
| G4 Low entry effort | quality | ✔ | | **Selected as a constraint** on the four goals above |
| G1.4 Early warning / quirks | | ✔ | ✔ ownership of personal notes | Deferred: needs real sensor trends and an agreement on note ownership |
| G1.5 Alerts, G2.2 alert routing | | | ✔ | Deferred: needs live sensors; conflict C-3 kept |
| G1.6 MTBF, G1.7 PM | ✔ (Angela) | | | Deferred: they depend on G1.1 data existing first |
| G1.8 Spare parts | | ✔ | | Deferred: not linked to any conflict, so lower learning value |
| G2.3 Near miss / spill | | ✔ | | Deferred: separate workflow from repair; good V2 candidate |
| G3.2 / G3.3 Audit history & retrieval | ✔ | | | Deferred: G3.1 is partly met by auto-stamping in REQ-04/06 |
| G4.2 Voice note | | ✔ | ✔ noisy floor (I-4) | Deferred: feasibility risk, and P:G-72 asks for human review before sharing |
| G4.5 Nickname search | | ✔ | | Deferred: the mock list is short; it is shown as a label only |
| G5 Offline, G6 Distraction | quality | | ✔ | G5 deferred (no backend; conflict C-5 kept). G6 used as a design constraint on REQ-06 |

### Requirements in scope

| REQ | Goal | Requirement (summary) | Key evidence |
|-----|------|-----------------------|--------------|
| REQ-01 | G1.1, G4.3, G4.4 | Open a downtime event for a machine with its stop time. It opens automatically on a simulated sensor stop, or manually for presses without sensors. No other field is needed to open it. | T2-L63, T2-L80, T2-L18, T1-L92, T1-L83, T5-L16 |
| REQ-02 | G1.1 | Measure downtime in minutes from the stop until an operator confirms the first good part. The clock keeps running until then. | T2-L9, T2-L14, T2-L63, T10-L13 |
| REQ-03 | G1.2 | Close the event only when a reason code (from a short list), the stop time, and the first-good-part time are recorded. Show which fields are missing. | T2-L16, T5-L83, T10-L13, T10-L15 |
| REQ-04 | G1.3.1, G4.1 | While a repair is open, record what was found, what was done and tested, any temporary repair, and the next action or what to watch. Use a short note and an optional photo. Stamp each entry with technician and time. | T1-L29, T1-L39, T2-L38, T2-L40, T1-L85, T4-L82, T9-L26 |
| REQ-05 | G1.3.2 | At the press, show the machine's open or handled status, the repair timeline, who worked on it, what was tested, and the next action. List open repairs by machine and shift. | T1-L13, T1-L85, T1-L87, T2-L34, T4-L109, T7-L24, T10-L20 |
| REQ-06 | G2.1, G6 | Record lockout per energy source (who and when, zero energy verified). Block release, and so block first-good-part confirmation, until every lock is recorded as removed and a shift supervisor authorizes release. Record who authorized it and when. | T3-L14, T3-L38, T3-L50, T3-L57, T6-L81, T6-L111, T11-L14, T11-L22, T5-L76, T9-L10 |

## 4. Relationships and decisions (Step 2)

| # | Type | Between | Evidence | Decision |
|---|------|---------|----------|----------|
| R1 | Overlap | REQ-04 / REQ-05 (Teo G-10 + Angela G-66; Teo G-33 + Angela G-65) | T1-L85, T2-L34 | **Combine the data, keep two REQs.** One open-repair record. REQ-04 writes it and REQ-05 shows it. They stay separate because writing and viewing are tested separately. |
| R2 | Overlap | REQ-01 / REQ-02 (both G1.1) | T2-L80 | **Implement separately on one event.** Opening and measuring are different user actions. |
| R3 | Dependency | REQ-02, 03, 04, 06 → REQ-01 | — | All of them need an open event for a machine. |
| R4 | Dependency | REQ-05 → REQ-04 | — | The press view shows what REQ-04 recorded. |
| R5 | Dependency | REQ-03 → REQ-02 → REQ-06 | T3-L12 | The event closes only after first good part. If a lockout was applied, the first good part can only be confirmed after release (a locked-out press cannot produce). |
| R6 | Conflict C-1 | REQ-03 (required reason code) vs. G4 (minimal effort) | T2-L16 (Angela states both), T1-L83 | **Compromise.** Required only at closure, chosen from a short list. Never required to open an event or start isolation. |
| R7 | Conflict C-4 | REQ-03 coded field vs. REQ-04 free note/photo | T2-L9 "not just free-text", T1-L81, T1-L95 "neat boxes" | **Combine.** The coded reason is required. The note and photo add detail but never replace the code. |
| R8 | Conflict C-2 | G1 downtime vs. G2.1 safety hold | T2-L86, T3-L61, T3-L63 | **Prioritize safety.** The release gate cannot be bypassed. **Unresolved:** whether time held in lockout counts toward Angela's downtime minutes or is reported apart under a safety code. Ask Angela and Rob together. V1 keeps one clock running stop→first good part and marks the event "included LOTO hold". |
| R9 | Conflict C-6 | REQ-06 complete LOTO detail vs. G6 no distraction | T3-L50, T3-L27 | **Compromise.** One tap per energy source. The system stamps name and time automatically. Entries are made before or after hands-on work, not during it. |
| R10 | Inconsistency I-2 | When is a repair "done"? Angela: first good part. Teo: "ran a full shift without me" | T2-L9, T1-L90 | **Keep both, implement one.** Downtime ends at first good part (REQ-02). Teo's verified-fixed / reopen-after-next-shift (M:G-19/G-20) is **unresolved and deferred.** Closing the event does not mean the fix is verified. |
| R11 | Inconsistency I-3 | Face-to-face handover vs. system record | T1-L47, T2-L38 | **Keep both.** Face-to-face handover (G1.3.3) stays a human step. The system holds the auditable record. Acknowledgement by the incoming supervisor (T11-L22) is a V2 candidate. |
| R12 | Agent uncertainty | Who authorizes release? M-model flagged "shift supervisor" as an AI assumption | T11-L14, T5-L76, T10-L24 | **Resolved by cross-team evidence.** The shift supervisor authorizes release. Rob (T11) and Angela (T5, T10) both name a supervisor or approver. |
| R13 | Conflict (P model) | Personal notebook knowledge vs. shared record | T1-L49, P analysis §3 | **Out of scope, preserved.** The prototype never imports personal notes. |
| R14 | Conflicts C-3, C-5 | Alert suppression vs. safety alerts; offline sync vs. overwrite | M combined docstring | **Out of scope, preserved.** Revisit when G1.5 or G5 is selected. |
