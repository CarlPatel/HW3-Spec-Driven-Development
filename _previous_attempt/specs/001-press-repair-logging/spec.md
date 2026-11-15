# Feature Specification: Press Breakdown, Handover & Safe Release Logging

**Feature Branch**: `001-press-repair-logging`

**Created**: 2026-11-15

**Status**: Draft (V1)

**Input**: User description: the `/speckit-specify` prompt in `docs/speckit-prompts.md` §2
(sprint scope REQ-01..REQ-06, merged goals TG-2..TG-6, evidence from transcripts T1–T11).

**Context**: A plastics plant runs injection-molding presses over three shifts. Night technicians
repair presses while production waits. The plant manager needs reliable downtime and repair data,
and the EHS coordinator needs lockout/tagout (LOTO) records that cannot be skipped. Today, records
are spread across notebooks, an office PC, paper binders and verbal handoffs. As a result, checks
are repeated, reason codes are left blank, and LOTO details go missing between shifts.

**Actors**: Technician (Teo), Shift Supervisor (release authority), Plant Manager (Angela, data
consumer), EHS Coordinator (Rob, safety-record owner). Roles are chosen with an on-screen switcher.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Open a press and log a breakdown at the machine (Priority: P1)

A technician at a stopped press finds it by its floor nickname and sees what is already known:
status, open repair, next action, who worked on it, and what was tested. A machine event is
already open, either from the (mock) sensor stop or opened manually for a press without sensors.
The technician logs what was tested, what was changed and whether it held, with an optional note
and photo, without walking to a computer.

**Why this priority**: This is the core path that every other story builds on. Angela named the
downtime-and-repair event record as the one feature to build first (T2 L80). Teo says he will go
back to his notebook if logging is slow (T1 L81).

**Independent Test**: Search a press, open its event, and save one repair entry. The entry
appears in that press's history with name and time, and the downtime clock is running.

**Acceptance Scenarios** (REQ-01, REQ-02, REQ-03):

1. **Given** two presses nicknamed "Old Blue" on different lines, **When** the user searches
   "old blue", **Then** both appear with asset number and line, and tapping one opens that press.
2. **Given** Press 12 has an open repair, **When** its record opens, **Then** status, next action,
   last technician and tests already done are visible without further navigation.
3. **Given** a mock sensor stop on Press 17 at 02:14, **When** the event opens, **Then** the stop
   time is 02:14 and the downtime clock is running.
4. **Given** an offline press without sensors, **When** a technician opens an event manually with a
   stop time, **Then** the event is created and the press shows "no sensor" without raising a
   fault or warning.
5. **Given** an open event, **When** a technician answers the three prompts and attaches a photo,
   **Then** the entry is saved with technician name and time and appears in the repair history.

---

### User Story 2 - Hand the open repair to the next shift (Priority: P2)

When the shift changes during a repair, the incoming technician or supervisor opens the press and
sees a handover summary built from the repair entries. It shows machine condition, isolation
status, what was found and done, parts, temporary repairs, next action and what to watch. They
acknowledge taking it over.

**Why this priority**: Lost handoffs cost about an hour of downtime in every interview set
(T1 L44, T2 L40, T9 L20). Teo's measure of success is that nobody has to come find him to ask
whether the press was really fixed (T9 L28).

**Independent Test**: Seed an open repair with a temporary fix. Switch to the incoming user,
open the press, read the summary, and acknowledge it.

**Acceptance Scenarios** (REQ-05):

1. **Given** an open repair with a temporary seal and a pending pressure test, **When** the next
   shift opens the press, **Then** the handover shows "temporary seal" and "next: pressure test".
2. **Given** an unacknowledged handover, **When** the incoming user acknowledges it, **Then** their
   name and time are recorded and the handover is marked acknowledged.
3. **Given** a handover that has not been acknowledged, **When** anyone views the press, **Then** it
   is visibly flagged "handover not acknowledged".

---

### User Story 3 - Keep the press on safety hold until LOTO is complete and released (Priority: P3)

Before opening the press, the technician confirms the LOTO step in one action. The LOTO record
then captures, for each energy source, who applied the lock, when, zero-energy verification, and
who removed the lock. The press stays on safety hold until this record is complete and a Shift
Supervisor authorizes release.

**Why this priority**: Rob's non-negotiable control (T6 L111, T11 L22), confirmed by Angela
(T10 L26). It is P3 only because it builds on an open event. It MUST be in V1.

**Independent Test**: Use a seeded press with two energy sources. Try to release with one lock
still recorded as on, then complete the record and release as a supervisor.

**Acceptance Scenarios** (REQ-06):

1. **Given** a LOTO record where one energy source has no lock-removal entry, **When** a supervisor
   tries to release, **Then** release is rejected and that energy source is listed as missing.
2. **Given** a complete LOTO record, **When** a Technician tries to release, **Then** it is refused;
   **When** a Shift Supervisor releases, **Then** approver name and time are recorded and the hold
   clears.
3. **Given** a press that just stopped, **When** the technician confirms LOTO, **Then** no other
   field (including reason code) is required at that moment.

---

### User Story 4 - Close the event with a coded reason and accurate downtime (Priority: P4)

After the press is released and the operator confirms the first good part, the event can be
closed. Closing requires a reason code from a short quick list and both times. The system lists
anything missing.

**Why this priority**: This was Angela's biggest data gap in all three interview sets (T2 L16,
T5 L83, T10 L13). It comes last in the flow because it depends on release and first good part.

**Independent Test**: Try to close an event without a reason code (refused, missing items
listed), then pick a code and close it. Downtime minutes are correct.

**Acceptance Scenarios** (REQ-02, REQ-04):

1. **Given** an event with stop 02:14, **When** first good part is confirmed at 03:02, **Then**
   downtime shows 48 minutes.
2. **Given** an event with no reason code, **When** anyone tries to close it, **Then** closing is
   refused and "reason code" is listed as missing; **When** a code is picked, **Then** it closes.
3. **Given** a press still on safety hold, **When** someone tries to confirm first good part,
   **Then** it is refused because the press has not been released.

---

### Edge Cases

- Nickname search with no match: "no press found" and the search text is kept. Several matches:
  all are shown with asset number and line (T4 L125).
- A press already has an open event: no second event is opened. The user is taken to the
  existing one.
- First-good-part time earlier than the stop time is rejected with a message.
- Shift changes before the handover is acknowledged: the repair stays flagged as unacknowledged.
- Photo fails to attach: the repair entry still saves without it, and the user is told.
- Supervisor tries to release when LOTO was never started, or a lock is still on: rejected,
  with the missing items listed.
- Closing an event while the press is on safety hold is impossible (no first good part yet).

## Requirements *(mandatory)*

### Functional Requirements

FR numbers map one-to-one to REQ IDs (FR-00n = REQ-0n).

- **FR-001 (REQ-01)**: Users MUST be able to find a press by floor nickname (case-insensitive,
  partial match). Each result MUST show nickname, asset number and line. Opening a press MUST
  show current status, open repair, next action, last technician and tests already done on one
  screen.
- **FR-002 (REQ-02)**: The system MUST open a machine event automatically when a mock sensor stop
  is triggered, and MUST let a technician open one manually with a stop time for presses without
  sensors. The downtime clock MUST run from stop time until first good part is confirmed. Downtime
  MUST be shown in whole minutes. Presses without sensors MUST show "no sensor" and MUST NOT be
  treated as faulted.
- **FR-003 (REQ-03)**: Technicians MUST be able to save a repair entry by answering three short
  prompts: what was tested, what was changed, and did it hold (yes / no / watching). They MAY add a
  free note and one photo. No other field is required. Each entry records technician name and time.
- **FR-004 (REQ-04)**: The system MUST refuse to close an event until a reason code (from a short
  quick list), stop time and first-good-part time are present, and MUST list what is missing. A
  reason code MUST NOT be required to open an event, confirm LOTO, or save a repair entry.
- **FR-005 (REQ-05)**: The system MUST show, on the press record, a handover summary built from the
  event's repair entries. It covers machine condition, isolation status, found, done, parts,
  temporary repairs, next action and what to watch. The incoming technician or supervisor MUST be
  able to acknowledge it, which records name and time. Unacknowledged handovers MUST be visibly
  flagged.
- **FR-006 (REQ-06)**: A press with an open LOTO MUST stay on safety hold. Release MUST be refused
  unless every energy source has: lock applied by (name), applied at (time), zero-energy verified,
  and lock removed by (name). Only the Shift Supervisor role MAY release, and approver name and time
  MUST be recorded. A refused release MUST list the missing items. First good part MUST NOT be
  confirmable while the press is on hold. Technicians MUST be able to confirm the LOTO step in one
  action before entering details.

### Key Entities

- **Press**: nickname, asset number, line, has-sensors flag, energy sources, status
  (running / down / on safety hold).
- **Machine Event**: press, source (sensor / manual), stop time, first-good-part time, reason code,
  state (open / closed), downtime minutes.
- **Repair Entry**: event, technician, time, tested, changed, held, optional note, optional photo,
  optional temporary-repair / next-action / watch fields.
- **LOTO Record**: event, per energy source: lock applied by, applied at, zero-energy verified,
  removed by. Plus release approver and release time.
- **Handover Acknowledgment**: event, incoming user, time.
- **Reason Code**: short seeded list.

### Traceability

| FR | REQ | Goal | Interview evidence |
|----|-----|------|--------------------|
| FR-001 | REQ-01 | TG-5 | T4 L122, T4 L125, T1 L83, T1 L85, T1 L87 |
| FR-002 | REQ-02 | TG-3 | T2 L9, T2 L63, T2 L80, T5 L16, T10 L13, T1 L92 |
| FR-003 | REQ-03 | TG-5 | T1 L81, T4 L78, T4 L80, T4 L82, T7 L10, T8 L28, T9 L12 |
| FR-004 | REQ-04 | TG-4 | T2 L16, T5 L83, T10 L13, T2 L71 |
| FR-005 | REQ-05 | TG-2 | T1 L7, T1 L44, T1 L47, T2 L38, T2 L40, T5 L25, T10 L20, T11 L22 |
| FR-006 | REQ-06 | TG-6 | T3 L14, T3 L38, T6 L81, T6 L111, T10 L24, T10 L26, T11 L22, T11 L28, T5 L41, T5 L76, T9 L10 |

Transcript key and merged goals: `docs/speckit-prompts.md`, `docs/goal-model.md`.

### Overlap, Dependency & Conflict Decisions

**Dependencies**

- REQ-02..REQ-06 depend on REQ-01: every workflow starts from the selected press.
- REQ-04 depends on REQ-02: an event with a stop time must exist before it can be closed.
- REQ-05 depends on REQ-03: the handover is built from the repair entries, with no separate form.
- REQ-02's first-good-part confirmation depends on REQ-06: no good part while on safety hold.

**Overlaps**

- **OV-1**: REQ-03 and REQ-05 both record the open repair state. All three source models merged
  Teo's "found / done / watch" goal into Angela's open-repair record. Decision: **combined**, as
  one record with two views.
- **OV-2**: Teo hands over technician-to-technician, face to face (T1 L47). Angela and Rob want a
  system record acknowledged by the incoming supervisor (T2 L38, T11 L22). Decision:
  **compromise**. The record supports either, and any incoming user may acknowledge it.

**Conflicts**

- **CF-1**: TG-4 (reason code and times required, Angela) conflicts with TG-5 (minimal entry during
  a breakdown, Teo). Angela states both sides herself (T2 L16). Decision: **compromise**. The
  reason code is required only at close and takes one tap from a quick list. It is never required
  at open or before isolation.
- **CF-2**: Coded fields, "not just free text" (T2 L9), conflict with Teo's "not a dozen boxes" and
  photo notes (T4 L35, T1 L81). Decision: **compromise**. The reason code and three prompts are
  structured; the free note and photo supplement them.
- **CF-3**: TG-7 (reduce downtime, Angela) conflicts with TG-6 (safety hold, Rob). Each warns about
  the other (T2 L86, T3 L61); Angela also says holds stay in place (T10 L26). Decision:
  **prioritize safety**, so the hold cannot be overridden. **Unresolved**: how hold time is
  counted. [NEEDS CLARIFICATION: Should time a press spends on safety hold count in the event's
  downtime minutes, or be reported separately under a safety category? Ask Angela, then confirm
  with Rob.]
- **CF-4**: Entry at the press (TG-5, T4 L94) conflicts with "tablets must not distract around
  moving machinery" (TG-8, T3 L27, T6 L113). Decision: **partial**. Detailed entry is expected
  while the press is stopped or locked out. **Unresolved** for running presses.
  [NEEDS CLARIFICATION: May a technician log observations on a running press (e.g. a warning
  sound) at the machine, or must they step to a safe location first? Ask Rob and Teo.]
- **I-1**: For Angela, downtime ends at first good part. For Teo, "fixed means it ran a full shift"
  (T1 L90). Decision: **keep both**. The clock stops at first good part, and "watch on next shift"
  is carried in the handover.

### Out of Scope (kept in the goal model)

- Sensor and safety alert routing (TG-12): needs live sensor integration.
- Offline capture and later sync (TG-10) versus no silent overwrite (TG-11): high uncertainty, and
  it cannot be demonstrated with mock data.
- Voice notes: the noisy floor (T2 L71) makes them a feasibility risk; photo only.
- Spare-part bin location, PM scheduling, MTBF and downtime reports, one-minute full history and
  inspection export, near-miss 24-hour reporting, chemical-spill reports, training records,
  supervisor escalation, and change audit trail.
- Copying Teo's personal notebook knowledge (TG-9; T1 L49, T4 L45, T9 L12). The record holds only
  the required repair facts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a walkthrough, a technician opens the correct press from its nickname in under
  10 seconds, without going through any intermediate screen. This is a team-set target; Teo asked
  only not to "hunt for the machine" (T1 L83).
- **SC-002**: A repair entry (three prompts) is saved in under 30 seconds. This is a team-set
  prototype target; stakeholders said only "a few seconds" (T8 L28).
- **SC-003**: 100% of closed events have stop time, first-good-part time, reason code, technician
  and completed work. Angela's one-year target is at least 95% (T2 L77).
- **SC-004**: In acceptance testing, 0 attempts to release a press with incomplete LOTO succeed,
  and 0 Technician-role release attempts succeed.
- **SC-005**: Downtime minutes equal the stop-to-first-good-part interval in 100% of seeded
  scenarios.
- **SC-006**: In a walkthrough, the incoming user can state the open repair's status, next action
  and watch items from the handover alone, without asking the outgoing technician (T9 L28).

## Assumptions

- Mock data only: about 8 presses, including a duplicate nickname ("Old Blue") and two offline
  presses without sensors. There are a few seeded events and a scripted "sensor stop" trigger.
- No login: a role switcher selects Technician or Shift Supervisor plus a seeded name.
- Single plant and a single tablet session. Data may reset on reload.
- The reason-code quick list is seeded (hydraulic, electrical, heater/thermal, tooling, setup,
  material, operator, other). The exact list needs Angela's confirmation.
- Energy sources per press are seeded (e.g. electrical, hydraulic).
- First good part is confirmed by whoever holds the tablet, on the operator's behalf. Operators are
  not a separate role in V1.
