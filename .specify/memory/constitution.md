<!-- 1.2.0: user-approved V2 refinements F-01–F-05; preserve V1 and unresolved conflicts. -->
<!-- 1.1.0 amendment: align scope with existing 002 V1 specification; preserve original 001 draft. -->
<!--
Sync Impact Report
- Version change: template (unversioned) → 1.0.0
- Principles defined: I. Sprint Scope Only; II. Traceability Is Mandatory; III. Prototype With Mock
  Data; IV. Floor-First Simplicity; V. Safety Before Uptime; VI. Preserve Conflicts, Don't Delete Them
- Added sections: Prototype Constraints; Spec-Driven Workflow
- Removed sections: none
- Deferred TODOs: none
-->

# Equipment Maintenance Logging Prototype Constitution

## Core Principles

### I. Sprint Scope Only

The prototype MUST implement only the requirements selected for the sprint in
`docs/goal-model.md` (REQ-01 to REQ-09; V2 authoritative scope: specs/003-v2-record-integrity/spec.md; V1: specs/002-maintenance-reliability-safety/spec.md). The goal model has other goals, but they MUST NOT be
built unless the spec is revised first. Any behavior the agent adds beyond the spec MUST be
removed or written down as an explicit assumption.
Rationale: the sprint shows that a small, coherent slice works. It is not meant to cover the
whole system.

### II. Traceability Is Mandatory

Every requirement MUST keep its REQ ID and link to a merged goal ID (G1.x) and to transcript
evidence (T#-L#). If Spec Kit numbers requirements as FR-xxx, the spec MUST keep an
FR ↔ REQ mapping. Every task and code component MUST name the REQ ID it implements.
Rationale: the traceability matrix in Step 4 depends on an unbroken chain from interview to
goal to spec to code.

### III. Prototype With Mock Data

The prototype MUST use mock data held in the client (machines, technicians, reason codes, and
simulated sensor stops). It has no real backend, no sensor integration, and no real
authentication. A simple user switcher stands in for login. Data MAY reset when the page
reloads.
Rationale: the sprint tests requirements, not infrastructure.

### IV. Floor-First Simplicity

Technicians work at the press, wearing gloves, in noise, under time pressure. Screens MUST favor
taps and short selections over typing. Nothing MUST block a technician from starting isolation
or repair. Required data is enforced at closure, not at opening.
Rationale: Teo (T1-L81, T1-L83) and Angela (T2-L71, T2-L84) warn that a slow tool gets worked
around, and then data quality falls apart.

### V. Safety Before Uptime

When safety and downtime goals conflict, safety controls (lockout/tagout recording and release
authorization) take priority. No convenience feature may bypass a safety gate.
Rationale: Rob (T3-L10, T3-L63) says "production can wait; an injury can't." This is the
documented team decision for conflict C-2.

### VI. Preserve Conflicts, Don't Delete Them

Conflicts between goals that the team has not resolved MUST stay visible in the spec and goal
model, together with the decision taken (prioritize, compromise, or leave unresolved). The
agent MUST NOT quietly resolve an open conflict.
Rationale: the assignment grades human judgment on conflicts, and keeping them visible
preserves the evidence.

## Prototype Constraints

- Single-page web prototype; desktop and tablet-width layouts only.
- Three demo roles via the user switcher: Technician, Shift Supervisor, Operator.
- At least one mock press has no sensors (offline 1990s press) so the manual path can be shown.
- No offline sync, notifications, analytics dashboards, or PM scheduling in this sprint.

## Spec-Driven Workflow

- Order: constitution → specify → clarify → human review → plan → tasks → implement.
- `spec.md` states what and why. The tech stack appears only in `plan.md`.
- Behavior changes are made in `spec.md` first, then carried into plan, tasks, and code.
- Acceptance scenarios use Given/When/Then and must be testable without asking the author.

## Governance

This constitution overrides agent defaults. Amendments must be recorded with a version bump
(MAJOR: principle removed or redefined; MINOR: principle added; PATCH: wording). Every review
of spec, plan, tasks, and code checks Principles I, II, and VI.

**Version**: 1.2.0 | **Ratified**: 2026-11-15 | **Last Amended**: 2026-11-18
