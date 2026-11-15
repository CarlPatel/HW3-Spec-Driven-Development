# Feature Specification: Maintenance Event Logging at the Press

**Feature Branch**: `001-maintenance-event-logging`

**Created**: 2026-11-15

**Status**: Draft (V1)

**Input**: User description: sprint-scope prompt in `docs/speckit-specify-prompt.md`
(REQ-01 to REQ-06, goals G1.1, G1.2, G1.3, G2.1 and quality goal G4 from `docs/goal-model.md`).

## Context

Night-shift technicians, operators and shift supervisors at an injection-molding plant need to
log machine stops, repairs and lockout/tagout on a tablet at the press. Today these records are
split across paper, notes, sensor history and verbal handovers. As a result, reason codes go
missing (T2-L14, T5-L83), the next shift repeats checks that were already done (T1-L44, T2-L40),
and lockout records have gaps between shifts (T6-L30, T6-L73). This prototype shows only the
sprint slice: one complete downtime event per machine stop, the open-repair handover record, and
a lockout/release gate.

## Stakeholder Goals in Scope

| Goal | Statement | Owner | Evidence | Requirements |
|------|-----------|-------|----------|--------------|
| G1.1 | Complete downtime and repair event tied to the machine | Angela Novak (plant manager) | T2-L80, T2-L63, T2-L9 | REQ-01, REQ-02 |
| G1.2 | Event closed only with reason code and times | Angela Novak | T2-L16, T5-L83, T10-L13 | REQ-03 |
| G1.3 | Repair not restarted from scratch after a shift change | Teo Salinas (technician), Angela Novak | T1-L32, T2-L40, T4-L109 | REQ-04, REQ-05 |
| G2.1 | Hazardous energy controlled during service | Rob Kessler (EHS) | T3-L14, T3-L50, T6-L111, T11-L14, T11-L22 | REQ-06 |
| G4 (quality) | Minimize tablet entry effort during a breakdown | Teo Salinas, Angela Novak | T1-L81, T1-L83, T2-L71 | Constraint on all REQs |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record a machine stop as one complete downtime event (Priority: P1)

A press stops. An event opens for that machine with the stop time, either automatically from
the sensor or by a technician tapping "Report stop" on a press without sensors. The technician
works the problem without filling in any form. When production resumes, the operator confirms
the first good part, and the system shows downtime in minutes. The technician closes the event
by choosing a reason code. If anything required is missing, the system says what.

**Why this priority**: Angela named this as the one feature to build first (T2-L80). Every
other story attaches to this event.

**Independent Test**: Simulate a stop on a sensor press, confirm first good part, try to close
without a reason code, then close with one. The result is an event with correct downtime minutes
and a reason code.

**Acceptance Scenarios**:

1. **(REQ-01)** **Given** Press 17 has sensors and is running, **When** a sensor stop is simulated at 02:14, **Then** an open event for Press 17 appears with stop time 02:14, source "sensor", and no fields required.
2. **(REQ-01)** **Given** Press 3 has no sensors, **When** a technician taps "Report stop" on Press 3, **Then** an event opens with the current time as stop time, marked "manual – no sensor", and no sensor-fault or missing-data warning appears.
3. **(REQ-01)** **Given** Press 17 already has an open event, **When** another sensor stop is simulated for Press 17, **Then** no second event is opened and the existing open event is shown.
4. **(REQ-02)** **Given** an open event on Press 17 stopped at 02:14 with no lockout applied, **When** the operator confirms first good part at 03:02, **Then** downtime shows 48 minutes and the downtime clock stops.
5. **(REQ-02)** **Given** an open event stopped at 02:14, **When** first good part has not been confirmed, **Then** the event shows a running downtime value that increases with elapsed whole minutes.
6. **(REQ-03)** **Given** an open event with first good part confirmed but no reason code, **When** the technician taps Close, **Then** closing is refused and "Reason code" is listed as missing.
7. **(REQ-03)** **Given** the same event, **When** the technician selects "Hydraulic" from the reason list and taps Close, **Then** the event closes and shows stop time, first-good-part time, downtime minutes and reason code.
8. **(REQ-03)** **Given** an open event with no first good part confirmed, **When** the technician taps Close, **Then** closing is refused and "First good part" is listed as missing.

---

### User Story 2 - Lock out and release the machine safely (Priority: P2)

Before opening the press, the technician records a lock on each hazardous-energy source with
one tap per source and confirms zero energy. The system stamps their name and the time. After
the repair, each lock removal is recorded, and the shift supervisor authorizes release. Until
then, the press cannot be confirmed as producing.

**Why this priority**: Rob's top priority is zero injuries (T3-L5). REQ-02 cannot finish on a
locked-out press, so this story must come before the event can be completed whenever service
needs isolation.

**Independent Test**: On an open event, apply two locks, try to confirm first good part
(blocked), remove the locks, authorize release as supervisor, then confirm first good part
(allowed). The record lists every applier, remover and authorizer with times.

**Acceptance Scenarios**:

1. **(REQ-06)** **Given** an open event on Press 12, **When** Teo taps "Lock applied" for Hydraulic and Electrical and confirms zero energy, **Then** each lock shows "Teo, <time>" and the machine shows status "Locked out".
2. **(REQ-06)** **Given** Press 12 has locks applied, **When** the operator tries to confirm first good part, **Then** it is blocked with "Release not authorized".
3. **(REQ-06)** **Given** both locks on Press 12 are recorded as removed, **When** a user in the Technician role taps "Authorize release", **Then** it is refused because only a Shift Supervisor may authorize release.
4. **(REQ-06)** **Given** both locks are recorded as removed, **When** the Shift Supervisor authorizes release, **Then** release is recorded with supervisor name and time, and first-good-part confirmation becomes available.
5. **(REQ-06)** **Given** one lock is still applied, **When** the Shift Supervisor tries to authorize release, **Then** it is refused and the remaining lock is listed.
6. **(REQ-06, REQ-03)** **Given** an event with locks still applied, **When** the technician taps Close, **Then** closing is refused and "Lockout not released" is listed as missing.

---

### User Story 3 - Hand over an open repair so the next shift does not start from zero (Priority: P3)

While a repair is open, the technician adds short entries: what was found, what was done or
tested, any temporary repair, and the next action or what to watch. A photo is optional. The
next technician opens that machine at the press and sees the status, timeline, who worked on it
and the next action first. A list shows all open repairs by machine and shift.

**Why this priority**: All three teammate models include it, and it prevents the hour lost on
Molder 8 (T2-L40) and Press 12 (T1-L44). It depends on User Story 1, because entries attach to
an event.

**Independent Test**: As night technician, add an entry with a temporary repair and a next
action to an open event. Switch to day technician and open the machine. The status, timeline,
author and next action are visible without searching.

**Acceptance Scenarios**:

1. **(REQ-04)** **Given** an open event on Molder 8, **When** Teo adds "Temporary seal installed" as temporary repair and "Pressure test" as next action with a photo, **Then** the entry appears with "Teo, <time>", the photo, and the next action.
2. **(REQ-04)** **Given** an open event, **When** a technician saves an entry with only a photo and no text, **Then** the entry is saved. **When** they try to save an entry with no text and no photo, **Then** it is not saved.
3. **(REQ-05)** **Given** Molder 8 has an open repair logged on night shift, **When** the day technician opens Molder 8, **Then** the top of the view shows status "Open", the latest next action "Pressure test", who worked on it, and tests done, followed by the full timeline.
4. **(REQ-05)** **Given** open repairs exist on Molder 8 (night) and Press 12 (day), **When** any user opens the open-repairs list, **Then** each appears with machine, shift of last entry, last technician and next action.
5. **(REQ-05)** **Given** an event has been closed, **When** a user opens that machine, **Then** its status shows "Handled" with the closed event in its history.

---

### Edge Cases

- A sensor stop on a machine that already has an open event does not create a duplicate (US1-3).
- A first-good-part time earlier than the stop time is rejected with a message.
- An attempt to close while locks are applied is refused, and the lockout is listed as missing (US2-6).
- A lock may be removed by a different person than the one who applied it. Both names are recorded.
- An entry with neither text nor photo is not saved (US3-2).
- Release authorization by a non-supervisor role is refused (US2-3).
- A machine without sensors shows no sensor data area and no "missing data" error (US1-2).
- If a reason code is chosen before first good part, it is kept, and closing still waits for first good part.

## Requirements *(mandatory)*

### Functional Requirements

| FR | REQ | Goal |
|----|-----|------|
| FR-001 – FR-003 | REQ-01 | G1.1, G4 |
| FR-004 – FR-005 | REQ-02 | G1.1 |
| FR-006 – FR-007 | REQ-03 | G1.2, G4 |
| FR-008 – FR-009 | REQ-04 | G1.3, G4 |
| FR-010 – FR-011 | REQ-05 | G1.3 |
| FR-012 – FR-015 | REQ-06 | G2.1 |

- **FR-001 (REQ-01)**: When a sensor stop is detected (simulated) on a machine with sensors, the system MUST open a downtime event for that machine recording the stop time and source "sensor".
- **FR-002 (REQ-01)**: Technicians and operators MUST be able to open a downtime event manually for any machine. The stop time defaults to now, and the source is "manual". For machines without sensors this is the only path, and no sensor-fault or missing-data indication is shown.
- **FR-003 (REQ-01, G4)**: Opening an event MUST require no input other than the machine. A machine MUST NOT have more than one open event.
- **FR-004 (REQ-02)**: The system MUST compute downtime in whole minutes from stop time to first-good-part time. While first good part is unconfirmed, it MUST show the elapsed downtime as running.
- **FR-005 (REQ-02)**: Operators MUST be able to confirm first good part on an open event. A first-good-part time earlier than the stop time MUST be rejected.
- **FR-006 (REQ-03)**: The system MUST refuse to close an event unless a reason code, stop time and first-good-part time are recorded and no lock is still applied. A refusal MUST list each missing item.
- **FR-007 (REQ-03, G4)**: The reason code MUST be picked from a fixed list. Free text MUST NOT substitute for it. The list: Hydraulic, Electrical/Heater, Mechanical, Material, Setup/Changeover, Operator, Safety hold, Other.
- **FR-008 (REQ-04)**: While an event is open, technicians MUST be able to add entries with any of: what was found, what was done/tested, temporary repair, and next action / what to watch, plus an optional photo. An entry needs at least text or a photo.
- **FR-009 (REQ-04)**: Each entry MUST be stamped automatically with the technician's name and time. Users MUST NOT type their name or the time.
- **FR-010 (REQ-05)**: The machine view MUST show, before the full timeline: status (Open / Locked out / Handled), the latest next action, the technicians who worked on the event, and the tests recorded.
- **FR-011 (REQ-05)**: The system MUST provide a list of all open repairs showing machine, shift of the latest entry, latest technician and next action.
- **FR-012 (REQ-06)**: Technicians MUST be able to record a lock as applied for each energy source of the machine with one action, plus a zero-energy confirmation. Name and time are stamped automatically.
- **FR-013 (REQ-06)**: Technicians MUST be able to record each lock as removed. Remover name and time are stamped automatically and may differ from the applier.
- **FR-014 (REQ-06)**: Only a Shift Supervisor MUST be able to authorize release, and only when every applied lock is recorded as removed. The authorizer and time are recorded.
- **FR-015 (REQ-06, C-2)**: If any lock was applied on an event, first-good-part confirmation MUST be blocked until release is authorized. The event MUST be marked "included LOTO hold".

### Key Entities

- **Machine**: a press or molder. Has a name, an asset number, a line, whether it has sensors, and its energy sources. Has at most one open event.
- **Downtime Event**: one stop of one machine. Holds stop time, source (sensor/manual), first-good-part time, downtime minutes, reason code, status (open/closed), and the LOTO-hold flag.
- **Repair Entry**: a stamped note on an event. Holds found, done/tested, temporary repair, next action, optional photo, technician, time and shift.
- **Lock Record**: one energy source on one event. Holds applier, applied time, zero-energy confirmed, remover, removed time.
- **Release Authorization**: the supervisor's approval to return the machine to production, with name and time.
- **User**: a demo person with a role (Technician, Operator, Shift Supervisor) and a shift.

## Overlap, Dependency and Conflict Decisions

**Overlaps**
- REQ-04 and REQ-05 both serve G1.3 (Teo's handover note M:G-33/G-10 + Angela's open-repair visibility M:G-65/G-66). One record is used: REQ-04 writes it and REQ-05 shows it. They stay separate because writing and viewing are tested separately.
- REQ-01 and REQ-02 both serve G1.1. They are separate actions on one event.

**Dependencies**
- REQ-02, REQ-03, REQ-04 and REQ-06 depend on REQ-01 (an open event must exist).
- REQ-05 depends on REQ-04 (it shows those entries).
- REQ-03 depends on REQ-02 (first-good-part time is required to close).
- REQ-02 depends on REQ-06 when locks are applied (a locked-out press cannot produce a good part).

**Conflicts**

| ID | Conflict | Decision |
|----|----------|----------|
| C-1 | Angela wants a required reason code (REQ-03). Teo and Angela want no blocking fields during a breakdown (G4) (T2-L16, T1-L83). | **Compromise**: required only at closure, picked from a short list. Never required to open an event or apply a lock (FR-003, FR-006). |
| C-4 | Angela wants a coded reason, "not just free-text" (T2-L9). Teo wants quick notes/photos (T1-L81). | **Combine**: the code is required, and notes and photos supplement it (FR-007, FR-008). |
| C-2 | Angela wants downtime reduced. Rob: "safety requirements aren't watered down" (T2-L86, T3-L61). | **Prioritize safety**: the release gate cannot be bypassed (FR-014, FR-015). **UNRESOLVED – needs Angela and Rob together**: whether lockout-hold time counts in downtime minutes or is reported apart under "Safety hold". V1 interim: one stop-to-first-good-part clock, event flagged "included LOTO hold". |
| C-6 | Rob wants complete LOTO detail (T3-L50) but no tablet distraction near moving equipment (T3-L27). | **Compromise**: one action per energy source, with name and time auto-stamped (FR-012, FR-013). |
| I-2 | Angela: downtime ends at first good part (T2-L9). Teo: "Fixed means it ran a full shift without me" (T1-L90). | **Keep both, implement one**: V1 implements Angela's definition. Teo's verified-fix/reopen-after-next-shift is **UNRESOLVED and out of scope**. Closing an event does not mean the fix is verified. |
| I-3 | Face-to-face handover (T1-L47) vs. auditable system record (T2-L38). | **Keep both**: face-to-face stays a human step. The system holds the record (REQ-04/05). |
| R12 | Who authorizes release? (marked as an assumption in the `Model/` combined model) | **Resolved by cross-team evidence**: Shift Supervisor (T11-L14, T5-L76). |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (REQ-01)**: A technician opens a manual event for a machine without sensors in 2 taps or fewer from the machine list.
- **SC-002 (REQ-02)**: In 100% of the demo scenarios, displayed downtime minutes equal the minutes between stop time and first-good-part time.
- **SC-003 (REQ-03)**: 100% of closed events have a reason code, stop time and first-good-part time. Angela's one-year target is ≥95% (T2-L77); the prototype enforces it for every closure.
- **SC-004 (REQ-04)**: A technician adds a repair entry with a next action in under 30 seconds without typing more than one short line.
- **SC-005 (REQ-05)**: An incoming technician who did not do the work can state the open repair's next action and who last worked on it within 30 seconds of opening the machine, without asking anyone.
- **SC-006 (REQ-06)**: 0 machines can be confirmed producing or closed while a lock is still applied or release is unauthorized.

## Assumptions

- Prototype only: mock data for about 6 machines (at least one without sensors, e.g. a 1990s press), 3 shifts (Day, Swing, Night), and demo users. No login; a role switcher selects Technician, Operator or Shift Supervisor.
- Sensor stops are simulated with a demo control. There is no real sensor integration.
- The reason-code list is a draft for Angela to confirm. "Safety hold" is included so C-2 can be recorded either way.
- Energy sources per machine are drawn from electrical, hydraulic and pneumatic.
- Data may reset on page reload. There is no offline sync or change history in V1.
- Shift is taken from the demo user's assigned shift.

## Out of Scope

- G1.4 early-warning drift and press quirk notes. G1.5 / G2.2 alerts and alert routing (conflict C-3 kept in the goal model).
- G1.6 MTBF / root-cause reports. G1.7 PM scheduling. G1.8 spare-part locations.
- G2.3 near-miss and chemical-spill reports.
- G3.2 change history / no silent overwrite. G3.3 full audit-record retrieval.
- G4.2 voice notes (noisy-floor feasibility risk, I-4). G4.5 nickname search.
- G5 offline operation and sync (conflict C-5 kept in the goal model).
- Incoming-shift acknowledgement of the handover (T11-L22): V2 candidate.
- Teo's verified-fixed / reopen-after-next-shift (M:G-19/G-20): unresolved, see I-2.
- Real authentication, backend, and sensor integration.
