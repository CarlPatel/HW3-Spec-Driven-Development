# 17-626 HW3 — Spec-Driven Development

**Team:** Timothy Zhang, Carl Patel, Austin Huang
**System:** Pressroom maintenance logging, shift handover, and lockout/tagout records.

## Required submission links

| Required component | Direct link |
|---|---|
| 1. GitHub Version 1 — original model, specification, planning and source | [V1 branch](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v1) · [preserved V1 commit](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/bef8e6c0bfae46af486e561841c32f9c8d159b88) |
| 2. GitHub Version 2 — revised model, specification, planning and source | [V2 branch](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v2) · [preserved V2 commit](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/e304dfaaaa851da39d8733af716116b78d66ad8a) |
| 3. Prototype V1 | [Open V1](https://carlpatel.github.io/HW3-Spec-Driven-Development/v1/) |
| 4. Prototype V2 | [Open V2](https://carlpatel.github.io/HW3-Spec-Driven-Development/v2/) |
| 5. Requirements Analysis and Learning Log | [Team-authored learning-log.md](learning-log.md) — requirements selection, relationships, V1 evaluation, revisions and reflection |

[Compare both deployed prototypes](https://carlpatel.github.io/HW3-Spec-Driven-Development/).
All submission artifacts are present on this default branch. V2 descends from V1;
the original version refs and frozen V1 application remain preserved.

## Requirements and evaluation evidence

- [V1 requirements traceability matrix](traceability.md)
- [V2 requirements traceability matrix](docs/traceability-v2.md)
- [V1 evaluation findings F-01–F-05](step4-evaluation/findings.md)
- [Browser observations and evidence](step4-evaluation/evidence/README.md)
- [Interview evidence locators](evidence/interview-evidence.csv)
- [V2 technical change map and verification limits](docs/v2-change-map.md)

## Goal models, specifications and Spec Kit artifacts

| Artifact | V1 | V2 |
|---|---|---|
| Goal model and scope/conflict decisions | [Frozen V1 model](versions/v1/goal-model.md) | [Revised model](docs/goal-model.md) |
| Specification | [002 V1 spec](specs/002-maintenance-reliability-safety/spec.md) | [003 V2 spec](specs/003-v2-record-integrity/spec.md) |
| Implementation plan | [V1 plan](specs/002-maintenance-reliability-safety/plan.md) | [V2 plan](specs/003-v2-record-integrity/plan.md) |
| Development tasks | [V1 tasks](specs/002-maintenance-reliability-safety/tasks.md) | [V2 tasks](specs/003-v2-record-integrity/tasks.md) |
| Data model | [V1 model](specs/002-maintenance-reliability-safety/data-model.md) | [V2 model](specs/003-v2-record-integrity/data-model.md) |
| Interface contract | [V1 contract](specs/002-maintenance-reliability-safety/contracts/ui.md) | [V2 contract](specs/003-v2-record-integrity/contracts/ui.md) |
| Run/acceptance walkthrough | [V1 walkthrough](specs/002-maintenance-reliability-safety/quickstart.md) | [V2 walkthrough](specs/003-v2-record-integrity/quickstart.md) |
| Source | [Frozen V1 app](versions/v1/frontend/) | [V2 app](frontend/) |

[Project constitution](.specify/memory/constitution.md). The earlier 001 draft remains
preserved as background; 002 is the evaluated V1 baseline and 003 revises it for V2.
The installed Spec Kit workflow/templates were applied; unavailable PowerShell helper
execution is disclosed in the plans rather than represented as an executed command.

## Run and check

Node 20+; no package installation or secrets.

```sh
npm test
npm run build
npm start
```

Open http://localhost:4183/ to compare V1 and V2. Both use independent in-memory mock
records and reset on reload. Demo roles and sensors are simulated. The build checks
V1 checksums and publishes both apps together. [Pages setup](docs/github-pages.md).

## Validation and remaining limits

24 V2 domain acceptance tests and the original 15 V1 tests pass. Saved technical
results and browser observations are in [V2 evidence](docs/v2-evidence/).
The application is a prototype, without real authentication, physical safety control,
live sensors, persistence or offline sync. Stakeholder safety policy and the reason-code
proxy for fault identity remain unconfirmed. Human SC-004/005 timing/comprehension
and browser photo selection/display remain outstanding; no full satisfaction claim
is substituted for those checks. C-2 (LOTO hold accounting) remains unresolved.

## Roles and Responsibilities

All three members collaborated on Steps 1–2 (requirements selection, merged goals,
and goal relationships) and jointly authored the supplied learning log.

- **Austin Huang:** Led Steps 1–2 and the consolidation of stakeholder data and goals;
  set up GitHub Spec Kit and generated the specifications from the combined inputs.
- **Carl Patel:** Used the specifications to build Prototype V1; implemented Prototype
  V2 from the evaluation findings and revised requirements; managed repository and
  deployment organization.
- **Timothy Zhang:** Led interaction with and evaluation of Prototype V1 and prepared
  the Requirements Traceability Matrix.
- **AI assistance:** Technical specification/planning, implementation, technical evaluation
  and verification support, and repository organization. The team-supplied learning
  log is included unchanged; no learning-log text was generated or rewritten here.

## Repository access

The instructor already has access, as confirmed by the team. The repository is
currently public at the team's request. The assignment specifies a private repository;
the team will confirm this visibility choice with the instructor. Both prototype
Pages links are accessible without signing in.
