/speckit.specify Build a prototype for ABC Design Services covering ONLY the following sprint scope. Keep my requirement IDs (REQ-xx) and goal IDs (G#.#) from docs/goal-model.md. Evidence refs are T#-L# (transcript, CSV line).

CONTEXT
Night-shift technicians, operators, and shift supervisors at an injection-molding plant log machine stops, repairs, and lockout/tagout on a tablet at the press. Today the records are split across paper, notes, and verbal handovers. As a result, reason codes are missing, shifts repeat each other's checks, and lockout records have gaps.

STAKEHOLDER GOALS AND REQUIREMENTS
- G1.1: Complete downtime and repair event tied to the machine. Owner: Angela (plant manager). Evidence: T2-L80, T2-L63, T2-L9.
  - REQ-01: The system shall open a downtime event for a specific machine with its stop time. It opens automatically when a (simulated) sensor detects a stop. For machines without sensors, a technician or operator opens it manually. No other field is needed to open it.
  - REQ-02: The system shall measure downtime in whole minutes from the stop until an operator confirms the first good part. The clock keeps running until that confirmation.
- G1.2: Event closed only with reason code and times. Owner: Angela. Evidence: T2-L16, T5-L83, T10-L13.
  - REQ-03: The system shall allow closing an event only when a reason code (picked from a short list), the stop time, and the first-good-part time are recorded. It shall show which items are missing.
- G1.3: Repair not restarted from scratch after a shift change. Owners: Teo (technician), Angela. Evidence: T1-L32, T2-L40, T4-L109.
  - REQ-04: While a repair is open, the system shall let a technician add entries for what was found, what was done or tested, any temporary repair, and the next action or what to watch. An entry is a short note with an optional photo. Each entry is stamped with technician name and time.
  - REQ-05: The system shall show, for a machine at the press, its status (open or handled), the entry timeline, who worked on it, what was tested, and the next action. It shall also list all open repairs by machine and shift.
- G2.1: Hazardous energy controlled during service. Owner: Rob (EHS). Evidence: T3-L14, T3-L50, T6-L111, T11-L14, T11-L22.
  - REQ-06: The system shall record lockout per energy source (applied by whom and when, zero energy verified). It shall block release, and therefore first-good-part confirmation, until every lock is recorded as removed and a shift supervisor authorizes release. It records who authorized release and when.
- Quality goal G4: minimize entry effort during a breakdown (Teo, Angela; T1-L81, T1-L83, T2-L71). Entries are taps or short text, and required data is enforced at closure only.

ACCEPTANCE SCENARIOS
- REQ-01: Given Press 17 has sensors and is running, when a sensor stop is simulated at 02:14, then an open event for Press 17 appears with stop time 02:14 and no fields required.
- REQ-01: Given Press 3 has no sensors, when a technician taps "Report stop" on Press 3, then an event opens with the current time as stop time, marked "manual – no sensor", and no sensor fault is shown.
- REQ-02: Given an event stopped at 02:14 is open, when the operator confirms first good part at 03:02, then downtime shows 48 minutes and the clock stops.
- REQ-03: Given an open event with first good part confirmed but no reason code, when the technician taps Close, then closing is refused and "Reason code" is listed as missing. When a code is chosen and Close is tapped again, the event closes.
- REQ-04: Given an open event on Molder 8, when Teo adds "temporary seal installed; next: pressure test" with a photo, then the entry appears with "Teo, <time>", the photo, and the next action.
- REQ-05: Given Molder 8 has an open repair from night shift, when the day technician opens Molder 8, then they see status Open, the timeline, who worked on it, the tests done, and "Next: pressure test" before anything else. The open-repairs list shows Molder 8 under Night shift.
- REQ-06: Given hydraulic and electrical locks are applied on Press 12, when the operator tries to confirm first good part, then it is blocked with "Release not authorized". After both locks are recorded as removed and the shift supervisor authorizes release, confirmation is allowed and the record shows each applier and remover, the authorizer, and their times.

ASSUMPTIONS
- Mock data only: about 6 machines (at least one without sensors), 3 shifts, demo users. No login; a role switcher selects Technician, Operator, or Shift Supervisor.
- Sensor stops are simulated by a demo button.
- Reason-code list (draft, to be confirmed by Angela): Hydraulic, Electrical/Heater, Mechanical, Material, Setup/Changeover, Operator, Safety hold, Other.
- Energy sources per machine: electrical, hydraulic, pneumatic (as applicable).
- Data may reset on page reload.

DEPENDENCIES
- REQ-02, REQ-03, REQ-04, REQ-06 depend on REQ-01 (they need an open event).
- REQ-05 depends on REQ-04 (it shows those entries).
- REQ-03 depends on REQ-02 (first-good-part time is required to close).
- REQ-02 depends on REQ-06 when locks are applied (a locked-out press cannot produce a good part).

EDGE CASES
- Sensor stop on a machine that already has an open event: do not open a duplicate.
- First good part entered before the stop time, or edited stop time after first good part: reject with a message.
- Close attempted while locks are still applied: refuse and list the lockout as missing.
- Lock removal by a different person than the applier: allowed, and both names are recorded.
- Note left empty with only a photo: allowed. Empty note and no photo: not saved.
- Release authorization attempted by a non-supervisor role: refused.
- Machine without sensors: no sensor data area, and no "missing data" error.

OVERLAP AND CONFLICT DECISIONS
- Overlap: REQ-04 and REQ-05 both serve G1.3 (Teo's handover note + Angela's open-repair visibility). One record is used: REQ-04 writes it, REQ-05 shows it.
- Overlap: REQ-01 and REQ-02 both serve G1.1. They are separate actions on one event.
- Conflict C-1: Angela wants a required reason code (REQ-03). Teo and Angela want no blocking fields during a breakdown (G4). Compromise: required only at closure, from a quick list, never to open an event or start lockout.
- Conflict C-4: coded reason (Angela) vs. quick note/photo (Teo). Combined: the code is required, and notes and photos supplement it.
- Conflict C-2: Angela wants minimal downtime. Rob says safety holds must not be watered down (T3-L61, T2-L86). Safety is prioritized: the release gate cannot be bypassed. UNRESOLVED, needs Angela + Rob: whether lockout-hold time counts in downtime minutes. V1 keeps one stop-to-first-good-part clock and flags the event "included LOTO hold". Keep this conflict documented in the spec.
- Conflict C-6: Rob wants complete LOTO detail but no tablet distraction. Compromise: one tap per energy source, with name and time auto-stamped.
- Inconsistency I-2: Angela says downtime ends at first good part. Teo says "fixed = ran a full shift" (T1-L90). V1 implements Angela's definition only. Teo's verified-fix/reopen is UNRESOLVED and out of scope; closing ≠ verified fixed.
- Release authorizer = shift supervisor, supported by T11-L14, T5-L76 (an earlier model had marked this as an assumption).

OUT OF SCOPE
- Early-warning drift and press quirk notes (G1.4); alerts and alert routing (G1.5, G2.2; conflict C-3 kept); MTBF/root-cause reports (G1.6); PM scheduling (G1.7); spare-part locations (G1.8); near-miss and spill reports (G2.3); change history / no-overwrite and full audit retrieval (G3.2, G3.3); voice notes (G4.2, noisy-floor risk); nickname search (G4.5); offline sync (G5; conflict C-5 kept); incoming-shift acknowledgement (V2 candidate); real login, backend, and sensor integration.
