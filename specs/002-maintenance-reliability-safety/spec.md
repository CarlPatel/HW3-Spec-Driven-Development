# Feature Specification: Downtime, Handover and Lockout Records at the Press

**Feature Branch**: `002-maintenance-reliability-safety`

**Created**: 2026-11-15

**Status**: Draft (V1 sprint scope: 15 goals)

**Input**: Merged team goal model (`docs/goal-model.md`), refined with the detailed goals in the
three teammate Assignment 2 models (M: `Model/`, C: Carl `Assignment 2/`, P: Timothy
`assignment-2/`) and the eleven interview transcripts T1–T11.

**Citation key**: `T#-L#` = transcript and CSV line (header = line 1), as defined in
`docs/goal-model.md` §1. `M:` / `C:` / `P:` + goal ID = goal in that teammate's combined model.

## Problem

An injection-molding plant runs presses across three shifts (Day 06–14, Swing 14–22, Night 22–06).
Today the downtime, repair and lockout records are split across paper, technician notebooks,
sensor history and verbal handovers (T2-L45, T2-L59, T3-L29). Because of this:

- Events are closed without reason codes (T2-L16, T5-L83).
- The next shift repeats checks that were already done. Molder 8 lost nearly an hour this way
  (T2-L40) and so did Press 12 (T1-L44).
- Lockout records are left incomplete across shift changes (T6-L30, T6-L73).
- Nobody records whether a fix actually held (T1-L90, T9-L20).

Three stakeholders are affected:

- **Teo Salinas** (night-shift technician) needs fast capture at the press with gloves on.
- **Angela Novak** (plant manager) needs complete, auditable downtime data.
- **Rob Kessler** (EHS coordinator) needs every isolation controlled and recorded.

## Stakeholder Goals in Scope (15)

Goals keep the merged `G#.#` scheme of `docs/goal-model.md`. Parent goals (G1, G2, G3, G4) are
context and are not counted.

| # | Goal | Statement | Owner | Model refs | Evidence | REQ |
|---|------|-----------|-------|-----------|----------|-----|
| 1 | G1.1 | Complete downtime and repair event tied to the machine | Angela | M:G-41 C:G-39 P:G-30 | T2-L80, T2-L63 | REQ-01, REQ-02 |
| 2 | G1.1.1 | Event opens automatically when a sensor detects a stop | Angela | M:G-51 C:G-7 | T2-L63, T2-L80 | REQ-01 |
| 3 | G1.1.2 | Stop reported manually when the press has no sensor | Teo | M:G-105, G-15 | T1-L92, T3-L24 | REQ-01 |
| 4 | G1.1.3 | Downtime measured in minutes from stop to first good part | Angela | M:G-46, G-52, G-53 P:G-33 | T2-L9, T2-L14, T10-L13 | REQ-02 |
| 5 | G1.2 | Event closed only with reason code and times | Angela | M:G-47, G-55 C:G-40, G-82 P:G-31, G-32 | T2-L16, T5-L83, T10-L13 | REQ-03 |
| 6 | G1.2.1 | Reason code picked from a short quick list | Angela, Teo | M:G-54 | T2-L9, T4-L35 | REQ-03 |
| 7 | G1.3.1 | Open-repair state recorded while the repair is open | Teo, Angela | M:G-65 C:G-7..G-12 P:G-9, G-10 | T1-L29, T2-L34, T2-L40 | REQ-04 |
| 8 | G1.3.2 | Open-repair state and history shown at the press | Teo | M:G-10 C:G-3, G-4 P:G-15 | T1-L85, T4-L109, T7-L24 | REQ-05 |
| 9 | G1.3.5 | Incoming shift acknowledges the handover | Rob, Angela | M:G-32 C:G-103 P:G-26, G-53 | T1-L47, T10-L11, T11-L22 | REQ-07 |
| 10 | G1.9 | Fix verified only after the next full shift without a repeat fault; otherwise reopened | Teo | M:G-9, G-19, G-20 C:G-11, G-29 P:G-19 | T1-L34, T1-L90, T9-L22 | REQ-08 |
| 11 | G2.1 | Hazardous energy controlled: lock per energy source, zero energy verified | Rob | M:G-83, G-84, G-85, G-102 C:G-87, G-98 P:G-49 | T3-L14, T3-L50, T6-L64 | REQ-06 |
| 12 | G2.1.1 | Release only after every lock is removed and a shift supervisor authorizes it | Rob, Angela | M:G-82, G-87, G-88 C:G-58 P:G-38, G-50, G-73 | T3-L57, T5-L76, T11-L14, T11-L22 | REQ-06 |
| 13 | G3.4 | Incomplete lockout records cannot be closed or handed over | Rob | M:G-114 C:G-101, G-102 P:G-52 | T6-L96, T6-L98, T6-L111 | REQ-09 |
| 14 | G4.1 | Quick note or photo instead of long typing | Teo | M:G-36 C:G-12, G-13 P:G-11, G-12 | T1-L81, T1-L85, T4-L82 | REQ-04 |
| 15 | G4.3 | Required fields never block opening an event or isolating a machine | Teo, Angela | M:G-37 | T1-L83, T2-L16 | REQ-01, REQ-06 |

### Why these 15

Rating criteria come from the HW3 handout:

- **Core**: without it the system has no purpose.
- **User-facing**: a stakeholder touches it on the floor.
- **Uncertain**: stakeholders disagree, or the evidence is incomplete.

| Goal(s) | Core | User-facing | Uncertain | Reason |
|---------|:----:|:-----------:|:---------:|--------|
| G1.1, G1.1.1, G1.1.3 | ✔ | ✔ | | Angela's "one feature first" (T2-L80). Every other goal attaches to this event. |
| G1.1.2 | ✔ | ✔ | ✔ | I-1: Angela assumes sensors exist. Teo has 1990s presses without them (T1-L92). |
| G1.2, G1.2.1 | ✔ | ✔ | ✔ | C-1 and C-4: required code vs. low effort and free notes. |
| G1.3.1, G1.3.2 | ✔ | ✔ | | Named in all three teammate models. Caused the lost hour on Molder 8 and Press 12. |
| G1.3.5 | | ✔ | ✔ | I-3: verbal vs. recorded handover. Rob asks for acknowledgment (T11-L22). |
| G1.9 | | ✔ | ✔ | I-2: "done" means first good part (Angela) or a full shift without a repeat (Teo). |
| G2.1, G2.1.1 | ✔ | ✔ | ✔ | Rob's top priority (T3-L5). C-2: uptime vs. safety hold. |
| G3.4 | ✔ | ✔ | | Rob: incomplete LOTO records must not be handed off or closed (T6-L111). |
| G4.1, G4.3 | | ✔ | ✔ | The quality side of C-1. Without these, Teo goes back to his notebook (T1-L81). |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record a machine stop as one complete downtime event (Priority: P1)

A press stops. An event opens with the stop time, either from the sensor or by someone tapping
"Report stop". The technician works the problem without filling in a form. The operator confirms
the first good part, and downtime appears in minutes. The event closes only with a reason code.

**Why this priority**: Angela named it as the one feature to build first (T2-L80). Every other
story attaches to this event.

**Independent Test**: Simulate a sensor stop on Press 17 and confirm first good part. Try to
close without a reason code (refused), then close with one.

**Acceptance Scenarios**:

1. **(REQ-01)** **Given** Press 17 has sensors and is running, **When** a sensor stop is simulated at 02:14, **Then** an open event for Press 17 appears with stop time 02:14, source "sensor", and no required fields.
2. **(REQ-01)** **Given** Old Blue has no sensors, **When** a technician taps "Report stop", **Then** an event opens with the current time, source "manual – no sensor", and no sensor-fault or missing-data warning.
3. **(REQ-01)** **Given** Press 17 already has an open event, **When** another sensor stop is simulated, **Then** no second event opens and the existing event is shown.
4. **(REQ-02)** **Given** an event stopped at 02:14 with no lockout, **When** the operator confirms first good part at 03:02, **Then** downtime shows 48 minutes and the clock stops.
5. **(REQ-02)** **Given** an event stopped at 02:14 without first good part, **When** the demo clock reads 02:44, **Then** the event shows a running downtime of 30 minutes.
6. **(REQ-02)** **Given** an event stopped at 02:14, **When** a first-good-part time of 02:10 is entered, **Then** it is rejected because it is earlier than the stop time.
7. **(REQ-03)** **Given** first good part is confirmed and no reason code is set, **When** the technician taps Close, **Then** closing is refused and "Reason code" is listed as missing.
8. **(REQ-03)** **Given** no first good part is confirmed, **When** the technician taps Close, **Then** closing is refused and "First good part" is listed as missing.
9. **(REQ-03)** **Given** first good part is confirmed, **When** "Hydraulic" is picked from the list and Close is tapped, **Then** the event closes showing stop time, first-good-part time, 48 minutes and "Hydraulic".

---

### User Story 2 - Lock out, verify and release the machine safely (Priority: P1)

Before opening the press, the technician records a lock on each energy source with one tap each
and confirms zero energy. After the repair, each removal is recorded and a shift supervisor
authorizes release. Until then the press cannot be confirmed as producing and the event cannot
close. An incomplete lockout record cannot be handed to the next shift.

**Why this priority**: Rob's top priority is zero injuries (T3-L5). "No lock, no work"
(T6-L140). The event in Story 1 cannot finish on a locked-out press.

**Independent Test**: On an open event, apply two locks and try first good part (blocked).
Remove the locks, authorize as supervisor, then confirm first good part (allowed).

**Acceptance Scenarios**:

1. **(REQ-06)** **Given** an open event on Press 12, **When** Teo taps "Lock applied" for Hydraulic and Electrical and confirms zero energy, **Then** each lock shows "Teo, <time>, zero energy verified" and Press 12 shows "Locked out".
2. **(REQ-06, G4.3)** **Given** a press is down, **When** a technician records a lock before any reason code or note exists, **Then** the lock is saved without asking for other fields.
3. **(REQ-06)** **Given** locks are applied, **When** the operator tries to confirm first good part, **Then** it is blocked with "Release not authorized".
4. **(REQ-06)** **Given** all locks are removed, **When** a Technician taps "Authorize release", **Then** it is refused because only a Shift Supervisor may authorize release.
5. **(REQ-06)** **Given** one lock is still applied, **When** the Shift Supervisor tries to authorize release, **Then** it is refused and the remaining lock is listed.
6. **(REQ-06)** **Given** all locks are removed (one by a different technician than the applier), **When** the Shift Supervisor authorizes release, **Then** release is recorded with name and time, both lock names are kept, and first good part becomes available.
7. **(REQ-09)** **Given** locks are still applied, **When** the technician taps Close, **Then** closing is refused and "Lockout not released" is listed as missing.
8. **(REQ-09)** **Given** a lock is applied without zero-energy confirmation, **When** the incoming technician tries to acknowledge the handover, **Then** acknowledgment is refused and "Zero-energy verification – Hydraulic" is listed as missing.
9. **(REQ-09)** **Given** both locks are applied with zero energy confirmed, **When** the incoming technician acknowledges the handover, **Then** it is accepted, and the acknowledgment lists each lock that is still applied with its applier.

---

### User Story 3 - Hand over an open repair so the next shift does not start from zero (Priority: P2)

While a repair is open, the technician adds short entries with a note or photo. The incoming
technician sees the status, tests done and next action first, then acknowledges the handover.

**Why this priority**: All three teammate models include it. It prevents the lost hour on
Molder 8 (T2-L40) and Press 12 (T1-L44). It depends on Story 1.

**Independent Test**: As night technician, add an entry with a next action. Switch to day
technician, open the machine, read the summary and acknowledge.

**Acceptance Scenarios**:

1. **(REQ-04)** **Given** an open event on Molder 8, **When** Teo adds "Temporary seal installed" as temporary repair and "Pressure test" as next action with a photo, **Then** the entry shows "Teo, <time>, Night", the photo and the next action.
2. **(REQ-04, G4.1)** **Given** an open event, **When** a technician saves an entry with only a photo, **Then** it is saved. **When** they save an entry with no text and no photo, **Then** it is not saved.
3. **(REQ-05)** **Given** Molder 8 has an open repair logged on Night shift, **When** the day technician opens Molder 8, **Then** the top of the view shows status "Open", next action "Pressure test", who worked on it and tests done, followed by the full timeline.
4. **(REQ-05)** **Given** open repairs on Molder 8 (Night) and Press 12 (Swing), **When** any user opens the open-repairs list, **Then** each shows machine, shift of last entry, last technician, next action and acknowledgment state.
5. **(REQ-07)** **Given** Molder 8's last entry is from Night shift, **When** the Day technician taps "Acknowledge handover" at 06:10, **Then** the record shows their name and 06:10, and the list shows "Acknowledged".
6. **(REQ-07)** **Given** Day shift starts at 06:00 and Molder 8 is not acknowledged, **When** the demo clock reads 06:29, then 06:30, **Then** at 06:29 it shows "Awaiting acknowledgment" and at 06:30 "Not acknowledged" (highlighted).

---

### User Story 4 - Verify that the fix held (Priority: P3)

Closing an event ends the downtime clock but does not mean the fix is verified. The repair is
verified after the next full shift with no repeat fault, or it is reopened.

**Why this priority**: It implements both sides of I-2. Teo: "Fixed means it ran a full shift
without me" (T1-L90). It depends on closed events with reason codes (Story 1).

**Independent Test**: Close a Hydraulic event during Night shift and advance the clock through
Day shift with no repeat (verified). Repeat with a second Hydraulic stop (reopened).

**Acceptance Scenarios**:

1. **(REQ-08)** **Given** a Hydraulic event on Press 17 closed with first good part at 03:02 (Night), **When** the demo clock reads 13:59, **Then** the repair shows "Awaiting verification".
2. **(REQ-08)** **Given** the same event and no new Hydraulic event on Press 17, **When** the clock reaches 14:00 (end of Day shift), **Then** the repair shows "Verified – ran full Day shift".
3. **(REQ-08)** **Given** the same event, **When** a new Hydraulic stop opens on Press 17 at 10:15, **Then** the earlier repair shows "Reopened – repeat fault" and the new event links to it.
4. **(REQ-08)** **Given** the same event, **When** a new Electrical/Heater stop opens on Press 17 at 10:15, **Then** the earlier repair is not reopened.

---

### Edge Cases

- A sensor stop on a machine that already has an open event does not create a duplicate (US1-3).
- A first-good-part time earlier than the stop time is rejected (US1-6).
- A reason code chosen before first good part is kept; closing still waits for first good part.
- A lock may be removed by a different person than the applier; both names are recorded (US2-6).
- Release authorization by a non-supervisor is refused (US2-4).
- A press may stay locked out across a shift change. Handover is allowed only if every applied lock has zero energy confirmed (US2-8, US2-9).
- An entry with neither text nor photo is not saved (US3-2).
- First good part exactly at a shift boundary (e.g. 06:00) belongs to the shift that starts then. Verification waits for the end of the next full shift (14:00 Swing → 22:00).
- A new stop with a different reason code does not reopen a repair (US4-4).

## Requirements *(mandatory)*

### Requirement map

| REQ | Summary | Goals | FRs |
|-----|---------|-------|-----|
| REQ-01 | Open an event (sensor or manual) with no other fields | G1.1, G1.1.1, G1.1.2, G4.3 | FR-001 – FR-003 |
| REQ-02 | Downtime from stop to first good part | G1.1, G1.1.3 | FR-004 – FR-005 |
| REQ-03 | Close only with reason code and times | G1.2, G1.2.1 | FR-006 – FR-007 |
| REQ-04 | Open-repair entries with note or photo | G1.3.1, G4.1 | FR-008 – FR-009 |
| REQ-05 | Open-repair view at the press and open-repairs list | G1.3.2 | FR-010 – FR-011 |
| REQ-06 | Lock per energy source and release gate | G2.1, G2.1.1, G4.3 | FR-012 – FR-015 |
| REQ-07 | Handover acknowledgment | G1.3.5 | FR-016 – FR-017 |
| REQ-08 | Fix verified or reopened | G1.9 | FR-018 – FR-019 |
| REQ-09 | Incomplete lockout blocks close and handover | G3.4 | FR-020 |

REQ-01 to REQ-06 keep the IDs used in spec 001.

### Functional Requirements

- **FR-001 (REQ-01)**: When a simulated sensor stop occurs on a machine with sensors, the system MUST open a downtime event with the stop time and source "sensor".
- **FR-002 (REQ-01)**: Any Technician or Operator MUST be able to open an event manually. The stop time defaults to now and the source is "manual". For machines without sensors this is the only path, and no sensor-fault or missing-data indication is shown.
- **FR-003 (REQ-01, G4.3)**: Opening an event MUST require no input other than the machine. A machine MUST NOT have more than one open event.
- **FR-004 (REQ-02)**: The system MUST compute downtime in whole minutes from stop time to first-good-part time and show it as running until first good part is confirmed.
- **FR-005 (REQ-02)**: Operators MUST be able to confirm first good part. A time earlier than the stop time MUST be rejected.
- **FR-006 (REQ-03)**: Closing MUST be refused unless reason code, stop time and first-good-part time are recorded and FR-020 is met. The refusal MUST list each missing item.
- **FR-007 (REQ-03, G1.2.1)**: The reason code MUST be picked from a fixed list: Hydraulic, Electrical/Heater, Mechanical, Material, Setup/Changeover, Operator, Safety hold, Other. Free text MUST NOT replace it.
- **FR-008 (REQ-04, G4.1)**: While an event is open, Technicians MUST be able to add entries with any of: found, done/tested, temporary repair, next action / what to watch, and an optional photo. An entry MUST contain at least text or a photo.
- **FR-009 (REQ-04)**: Each entry MUST be stamped automatically with the user's name, time and shift. Users MUST NOT type their name or the time.
- **FR-010 (REQ-05)**: The machine view MUST show, above the full timeline: status (Open / Locked out / Handled), latest next action, technicians involved, tests recorded, acknowledgment state and verification state.
- **FR-011 (REQ-05)**: The system MUST list all open repairs with machine, shift of latest entry, latest technician, next action and acknowledgment state.
- **FR-012 (REQ-06, G4.3)**: Technicians MUST be able to record a lock applied per energy source of the machine with one action each, plus a zero-energy confirmation. Name and time are stamped. No other field is required to record a lock.
- **FR-013 (REQ-06)**: Technicians MUST be able to record each lock removed. Remover and time are stamped and may differ from the applier.
- **FR-014 (REQ-06)**: Only a Shift Supervisor MUST be able to authorize release, and only when every applied lock is recorded as removed. Authorizer and time are recorded.
- **FR-015 (REQ-06, C-2)**: If any lock was applied on an event, first-good-part confirmation MUST be blocked until release is authorized. The event MUST be flagged "Included LOTO hold".
- **FR-016 (REQ-07)**: When an open event's latest entry or lock is from a previous shift, a Technician or Shift Supervisor of the current shift MUST be able to acknowledge the handover with one action. Name and time are stamped, and any locks still applied are listed with their appliers.
- **FR-017 (REQ-07)**: An open event not acknowledged within 30 minutes of the start of the current shift MUST be shown "Not acknowledged" and highlighted in the open-repairs list.
- **FR-018 (REQ-08)**: A closed event MUST show "Awaiting verification" until the end of the first full shift that starts at or after first good part. If no new event with the same reason code opens on that machine by then, it MUST become "Verified".
- **FR-019 (REQ-08)**: If a new event with the same reason code opens on that machine before verification, the earlier event MUST become "Reopened – repeat fault" and be linked to the new event.
- **FR-020 (REQ-09, G3.4)**: If a lock was applied on an event: (a) the event MUST NOT be closed unless every lock is removed and release is authorized; (b) the handover MUST NOT be acknowledged while any applied lock lacks zero-energy confirmation. Missing items MUST be listed.

### Key Entities

- **Machine**: name, floor nickname, asset number, line, has sensors, energy sources, status. Has at most one open event.
- **Downtime Event**: machine, stop time, source (sensor/manual), first-good-part time, downtime minutes, reason code, status (open/closed), LOTO-hold flag, verification state (Awaiting / Verified / Reopened), link to repeat event.
- **Repair Entry**: event, found, done/tested, temporary repair, next action, optional photo, author, time, shift.
- **Lock Record**: event, energy source, applier and time, zero-energy confirmed, remover and time.
- **Release Authorization**: event, shift supervisor, time.
- **Handover Acknowledgment**: event, acknowledging user, time, shift, locks still applied at that time.
- **User**: name, role (Technician, Operator, Shift Supervisor), shift.

## Overlap, Dependency and Conflict Decisions

**Overlaps**

| ID | Between | Decision |
|----|---------|----------|
| O-1 | REQ-04 / REQ-05 (Teo's handover note M:G-33/G-10 + Angela's open-repair state M:G-65/G-66) | **Combine data, keep separate REQs.** REQ-04 writes the one open-repair record and REQ-05 shows it. Writing and viewing are tested separately. |
| O-2 | REQ-01 / REQ-02 (both G1.1) | **Separate actions on one event.** |
| O-3 | REQ-06 release gate / REQ-09 incomplete-lockout gate | **Combine.** REQ-09 extends the REQ-06 gate to closing and handover. They stay separate because REQ-09 traces to Rob's records goal (G3.4) and REQ-06 to his energy-control goal (G2.1). |

**Dependencies**

- REQ-02 – REQ-07 and REQ-09 depend on REQ-01 (an event must exist).
- REQ-05 depends on REQ-04. REQ-07 depends on REQ-05 (the incoming technician acknowledges what the view shows).
- REQ-03 depends on REQ-02. REQ-02 depends on REQ-06 when locks are applied (a locked-out press cannot produce a good part).
- REQ-08 depends on REQ-03 (it compares reason codes of closed events).

**Conflicts** (no conflicting goal is deleted; each stays in the goal model)

| ID | Conflict | Decision |
|----|----------|----------|
| C-1 | Required reason code (G1.2) vs. minimal entry effort (G4.3) (T2-L16, T1-L83) | **Compromise**: required only at closure, from a short list. Never required to open an event or apply a lock (FR-003, FR-006, FR-012). |
| C-4 | Coded reason "not just free-text" (T2-L9) vs. quick notes/photos (G4.1, T1-L81) | **Combine**: code required at closure; notes and photos add detail but never replace it (FR-007, FR-008). |
| C-2 | Reduce downtime (G1) vs. safety hold (G2.1.1) (T2-L86, T3-L61) | **Prioritize safety**: the release gate cannot be bypassed (FR-014, FR-015). **UNRESOLVED – needs Angela and Rob together**: whether lockout-hold time counts in downtime minutes or is reported apart under "Safety hold". V1 interim: one clock, event flagged "Included LOTO hold". |
| C-6 | Complete LOTO detail (G2.1) vs. no tablet distraction (G6, deferred) (T3-L50, T3-L27) | **Compromise kept although G6 is deferred**: one action per energy source, name and time auto-stamped (FR-012, FR-013), so this sprint does not work against G6. |
| I-1 | Angela assumes sensors give the stop time; Teo has 1990s presses without sensors (T1-L92) | **Condition**: a manual path with no missing-data warning (FR-002). |
| I-2 | "Done" = first good part (T2-L9) vs. "ran a full shift without me" (T1-L90) | **Implement both**: first good part ends downtime (FR-004); verification after the next full shift (FR-018, FR-019). Closing does not mean verified. |
| I-3 | Face-to-face handover (T1-L47) vs. auditable record (T2-L38) | **Keep both**: face-to-face stays a human step (G1.3.3). The system holds the record and the acknowledgment (FR-016). |
| R12 | Who authorizes release? (marked as an AI assumption in the M combined model) | **Resolved by cross-team evidence**: Shift Supervisor (T11-L14, T5-L76). |

Conflicts C-3 (alert suppression vs. safety alerts), C-5 (offline sync vs. no overwrite), C-7
(stale telemetry vs. missing sensor data), C-8 (who may stop production), C-9 (PM vs. orders) and
C-10 (ownership of personal notes) involve only deferred goals. They are preserved in the goal
model and are not decided in this sprint.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (REQ-01)**: A technician opens a manual event for a machine without sensors in 2 taps or fewer from the machine list.
- **SC-002 (REQ-02)**: In 100% of demo scenarios, displayed downtime equals the whole minutes between stop and first good part.
- **SC-003 (REQ-03)**: 100% of closed events have reason code, stop time and first-good-part time. Angela's one-year target is ≥ 95% (T2-L77); the prototype enforces it for every closure.
- **SC-004 (REQ-04)**: A technician adds a repair entry with a next action in under 30 seconds, typing no more than one short line.
- **SC-005 (REQ-05, REQ-07)**: An incoming technician who did not do the work states the next action and who last worked on the repair within 30 seconds of opening the machine, without asking anyone, and acknowledges with one tap.
- **SC-006 (REQ-06, REQ-09)**: 0 events can be confirmed producing or closed while a lock is applied or release is unauthorized, and 0 handovers are acknowledged with an unverified lock.
- **SC-007 (REQ-08)**: In the demo data, every closed event ends in exactly one state: Awaiting verification, Verified or Reopened.

## Assumptions

Values marked **[confirm]** are prototype defaults chosen by the team. They are not stakeholder
statements and must be checked with the named stakeholder.

- Prototype only: mock data for about 6 machines, including at least one 1990s press without sensors ("Old Blue"). No login; a role switcher selects Technician, Operator or Shift Supervisor.
- Sensor stops are simulated with a demo control. A demo clock can be advanced to test shift and verification rules.
- Shifts: Day 06–14, Swing 14–22, Night 22–06 **[confirm with Angela]**.
- Reason-code list (FR-007) is a draft. "Safety hold" is included so C-2 can be recorded either way **[confirm with Angela]**.
- Handover acknowledgment window: 30 minutes into the shift (FR-017) **[confirm with Rob and Angela]**.
- A repeat fault means the same machine and the same reason code (FR-019) **[confirm with Teo]**.
- Energy sources per machine are drawn from electrical, hydraulic and pneumatic.
- Personal-lock transfer between shifts is a physical procedure outside the software. The system records only who applied and removed each lock.
- Data may reset on page reload. There is no offline sync or change history in V1.

## Out of Scope (deferred goals, preserved in the goal model)

| Deferred goal(s) | Reason |
|------------------|--------|
| G1.3.4 readings, tests and verification fields (Teo, T7-L26) | Strong V2 candidate. V1 keeps "done/tested" as a free entry. Evaluating V1 will show whether structured readings are needed. |
| G1.4.1 – G1.4.3 sensor trend, drift flag, press quirks | Need realistic sensor data. C-10 (ownership of personal notes) is unresolved. |
| G1.5, G1.5.1 condition alerts | Need live sensors; C-3 is preserved. |
| G1.6.1, G1.6.2 MTBF, repeat failures, root cause | Need a history of closed events that V1 starts to create. |
| G1.7.1, G1.7.2 PM checklists and scheduling | A separate workflow from breakdowns; C-9 is preserved. |
| G1.8 spare parts and awaiting parts | Not linked to a conflict, so lower learning value. |
| G1.10, G1.11 prioritization and escalation | Supervisor desk workflow; C-8 is preserved. |
| G2.2.1 – G2.2.3 stop work and unsafe-condition alerts | Large safety workflow of its own. V2 candidate with G2.3.1. |
| G2.3.1, G2.3.2, G2.4 near miss, spill, corrective actions | Separate EHS reporting workflow, not part of the repair event. |
| G3.1, G3.2, G3.3 audit trail, no silent overwrite, full record retrieval | Only partly met in V1, through auto-stamping (FR-009, FR-012 – FR-016). Change history needs persistence. |
| G4 (parent), G4.2 voice note, G4.4 stale or missing sensor data, G4.5 nickname search | G4 is covered by G4.1 and G4.3. G4.2 has a feasibility risk on a noisy floor (I-4). G4.4 has no sensor display in V1. G4.5: the mock list is short, so nicknames are shown as labels only. |
| G5 connectivity, G6 tablet distraction | G5 needs a backend (C-5 preserved). G6 is respected through C-6 but not tested. |
| Real authentication, backend and sensor integration | Prototype constraint. |
