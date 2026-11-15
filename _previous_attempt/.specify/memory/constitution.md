<!--
Sync Impact Report
- Version change: template → 1.0.0 (initial ratification)
- Principles defined: I. Prototype With Mock Data; II. Sprint Scope Discipline;
  III. Requirement Traceability; IV. No Invented Requirements, Preserved Conflicts;
  V. Safety Records Are Controls; VI. Floor-Usable Simplicity
- Added sections: Prototype Constraints; Development Workflow
- Removed sections: none
- Deferred TODOs: none
-->

# ABC Maintenance Logging Prototype Constitution

## Core Principles

### I. Prototype With Mock Data

The product is a prototype. It MUST run on mock data bundled with the app and MUST NOT depend
on a real backend, authentication, live sensors, or network synchronization. User roles
(Technician, Shift Supervisor) are chosen from an on-screen role switcher.
Rationale: the sprint evaluates requirements, not infrastructure.

### II. Sprint Scope Discipline

Only the requirements selected for the sprint (REQ-01 through REQ-06 for V1) MAY be implemented.
Any new behavior MUST first be added to the specification. Specification changes come before
code changes. Rationale: spec-driven development keeps the prototype faithful to the agreed scope.

### III. Requirement Traceability

Every requirement MUST keep its REQ ID and link to a merged goal ID (TG-n) and to transcript
evidence (T<n> L<line>). Functional requirement numbers in specs MUST map one-to-one to REQ IDs,
and implementation units MUST name the REQ they satisfy.
Rationale: supports the requirements traceability matrix.

### IV. No Invented Requirements, Preserved Conflicts

Agents MUST NOT add features or rules that stakeholders did not request. Gaps MUST be recorded as
Assumptions or `[NEEDS CLARIFICATION]` markers. Conflicting goals MUST stay documented with their
decision (prioritize, compromise, or unresolved) and MUST NOT be deleted.

### V. Safety Records Are Controls

No path MAY release equipment while its lockout/tagout record is incomplete, and production
pressure MUST NOT override a safety hold. Only an authorized supervisor role MAY release equipment.
Rationale: EHS stakeholder requirement; "no lock, no work, and no guessing."

### VI. Floor-Usable Simplicity

Screens MUST work at tablet size with large touch targets and the fewest required fields that
satisfy the requirements. Demonstrating the requirements takes precedence over visual polish.

## Prototype Constraints

- Data may reset on reload; persistence beyond the browser session is not required.
- No personal data beyond seeded fictional names.
- Deployment targets are static hosting; V1 and V2 MUST remain separately deployable.

## Development Workflow

- Order: constitution → specify → clarify → human review → plan → tasks → implement.
- Each spec is reviewed by hand for missing REQ IDs, invented requirements, testable
  Given/When/Then scenarios, and preserved conflict decisions before planning.
- V2 changes MUST start with a spec revision informed by V1 evaluation.

## Governance

This constitution overrides conflicting guidance in other artifacts. Amendments require a
documented reason, agreement from the team, and a semantic version bump (MAJOR: principle
removed or redefined; MINOR: principle or section added; PATCH: wording). Every plan and task
list MUST pass a constitution check before implementation.

**Version**: 1.0.0 | **Ratified**: 2026-11-15 | **Last Amended**: 2026-11-15
