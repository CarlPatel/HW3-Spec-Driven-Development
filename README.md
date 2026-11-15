# Pressroom — Maintenance Prototype V1

A tablet/desktop prototype for injection-molding maintenance: report a stop, record
repair work, control LOTO records, hand over to the next shift, and verify a fix.
Implements the existing **002 V1 specification: 15 goals, REQ-01–REQ-09**.

## Run

Node 20+; no package installation or account needed.

```sh
npm test
npm run build
npm start
```

Open http://localhost:4173. `dist/` is the deployable static build.
The demo starts at November 15, 2026, 06:10 in the browser's local timezone.
Use the user switcher for Technician, Operator and Shift Supervisor roles. The
clock can advance by minutes, hours, shift boundaries, or a chosen timestamp.
Reload or Reset demo restores sample data. All data, including photos, lives in memory.

## Assignment navigation

| Component | V1 status / link |
|---|---|
| GitHub V1 | [v1 branch](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v1) (see delivery record for push status) |
| GitHub V2 | Not created; reserved for the subsequent student evaluation/revision steps |
| Prototype V1 | Local: http://localhost:4173; external deployment awaiting permission, see [delivery record](docs/v1-delivery.md) |
| Prototype V2 | Not created |
| Requirements selection and goal relationships | [Merged goal model](docs/goal-model.md) |
| Specification | [Authoritative 002 V1 spec](specs/002-maintenance-reliability-safety/spec.md) |
| Plan and tasks | [Plan](specs/002-maintenance-reliability-safety/plan.md), [tasks](specs/002-maintenance-reliability-safety/tasks.md) |
| Implementation reference | [REQ → source map](docs/implementation-map.md) |
| Learning log and Step 4 evaluation | Student work remaining; no observations or learning-log answers generated |

The older [001 draft](specs/001-maintenance-event-logging/spec.md) remains preserved.
The 002 clarifications record exact shift-boundary behavior and delayed repeat-fault
classification; unresolved stakeholder assumptions and conflicts remain visible.

## Demo walkthrough

1. Old Blue: Report stop opens an event without required fields or sensor warnings.
2. Press 17: simulate a sensor stop twice; the same event remains selected.
3. Technician: apply a lock and verify zero energy. Operator: attempt first good part
   and see the release gate. Technician: record removal. Supervisor: authorize release.
4. Operator: confirm first good part. Technician: choose a reason, then close.
   Missing fields are listed if closure is attempted early.
5. Molder 8: inspect the next action/tests; select Maya (Day), acknowledge handover.
   Advance beyond 06:30 to see unacknowledged open repairs highlighted.
6. Close a coded repair and advance through its next full shift. A matching reason
   on a new stop before the verification deadline reopens the earlier repair with
   links in both directions. Code selection classifies the repeat using stop time.

## Validation and limitations

15 automated acceptance-rule tests cover REQ-01–09. Browser checks cover note entry,
manual stop, handover, lockout refusal, release roles, closure and verification at
tablet width. See [quickstart](specs/002-maintenance-reliability-safety/quickstart.md).
Student evaluation is still needed for comprehension and 30-second entry criteria.
This is a mock prototype, without authentication, a backend, live sensors, persistence,
or enforcement of physical safety procedures. Demo roles are selectable by anyone.

## Roles and Responsibilities

- Carl Patel: repository owner; existing course materials and requirements provided
  as inputs. Human evaluation and final contribution attribution remain to be recorded.
- Timothy: teammate identified in the supplied goal-model sources; existing model and
  interview packet used as requirements input. Confirm full name and contributions.
- Other group members: names and individual contributions were not supplied; the team
  must complete attribution before submission.
- AI development assistance: V1 scope alignment, technical planning, tasks, application,
  automated checks and run documentation. No learning-log authorship or student
  evaluation claims are included.
