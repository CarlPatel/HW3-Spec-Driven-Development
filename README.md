# Pressroom — V1 / V2 maintenance prototypes

V2 implements all five requirements refinements from the supplied Step 4 traceability
matrix. The initial V1 remains frozen and available for comparison. Both versions
are client-only mock prototypes; data resets on reload. No login or live sensors.

## Version history and organization

```text
v1: bef8e6c — original implementation and specification, unchanged
 └─ v2: 2177b9f — original traceability/evaluation + revised spec and goal model
         d072b14 — updated implementation and checks for findings F-01–F-05
```

V2 is a descendant of V1 in the same repository. On the `v2` branch:

- `traceability.md` preserves your original V1 evaluation matrix exactly.
- [docs/traceability-v2.md](docs/traceability-v2.md) connects the same requirement IDs
  and interview evidence to revised V2 requirements, implementation and checks.
- `frontend/` contains the updated V2 implementation, built from the V1 application.
- `specs/002-maintenance-reliability-safety/` preserves the original V1 specification.
- `specs/003-v2-record-integrity/` contains the V2 requirements and planning refinements.
- `versions/v1/` is the frozen copy used to keep the original `/v1/` prototype available
  beside `/v2/`; it is not a separately developed replacement for the V1 branch.

Check out `v1` to see the original submission state; check out `v2` to see V1 plus
the evaluation matrix, revised requirements and updated implementation.

## Run locally

Node 20+; no install or secrets.

```sh
npm test
npm run build
npm start
```

Open http://localhost:4183/ to compare versions, or /v2/ for the revised application.
The build checks V1 bytes against the frozen baseline before packaging both apps.

## Assignment navigation

| Deliverable | Link / status |
|---|---|
| GitHub V1 | [v1 source](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v1), baseline bef8e6c |
| GitHub V2 | [v2 source](https://github.com/CarlPatel/HW3-Spec-Driven-Development/tree/v2) |
| Prototype V1 | [V1 URL recorded in supplied evaluation](https://carlpatel.github.io/HW3-Spec-Driven-Development/v1/); frozen local copy /v1/ |
| Prototype V2 | Local http://localhost:4183/v2/; expected Pages /HW3-Spec-Driven-Development/v2/ after team deployment |
| Requirements / learning document | [User-supplied V1 matrix](traceability.md), [original evaluation findings](step4-evaluation/findings.md), [V2 technical change map](docs/v2-change-map.md); learning-log.md must be authored by the team |

Before submission, the team must place this navigation on the default branch and
replace pending links with actual deployed V2/source URLs. The default branch is not changed by this documentation update; verify the actual
V2 deployment before replacing pending deployment links.

## Specifications and planning

- [V1 spec and original plan](specs/002-maintenance-reliability-safety/)
- [V2 revised spec](specs/003-v2-record-integrity/spec.md),
  [plan](specs/003-v2-record-integrity/plan.md),
  [tasks](specs/003-v2-record-integrity/tasks.md),
  [walkthrough](specs/003-v2-record-integrity/quickstart.md)
- [V2 goal model refinements](docs/goal-model.md), [frozen V1 model](versions/v1/goal-model.md)
- [V2 traceability matrix](docs/traceability-v2.md) and
  [technical mapping and validation limits](docs/v2-change-map.md)
- [Dual-version GitHub Pages instructions](docs/github-pages.md)

## V2 behavior

- F-01: applicable energy-source decisions and historical isolation completeness.
- F-02: first-good-part time cannot precede recorded removal/release.
- F-03: fresh stops are recorded after production resumes, even with pending closeout.
- F-04: explicit incoming-shift acknowledgment persists after ordinary notes;
  critical isolation changes require reacknowledgment.
- F-05: repair verification needs an uninterrupted full recorded operating shift.
  Different-code stops interrupt that evidence; unknown codes remain pending.

The user approved these prototype defaults. Stakeholder policy remains unconfirmed;
reason categories remain a proxy for fault identity. Human SC-004/005 checks and
browser photo verification remain outstanding. See the change map for exact limits.

## Roles and Responsibilities

- Carl Patel: repository owner; existing course materials and requirements provided
  as inputs. Human evaluation and final contribution attribution remain to be recorded.
- Timothy: teammate identified in the supplied goal-model sources; existing model and
  interview packet used as requirements input. Confirm full name and contributions.
- Other group members: names and individual contributions were not supplied; the team
  must complete attribution before submission.
- AI development assistance: V1/V2 requirements alignment, technical planning, tasks, application,
  automated checks and run documentation. V2 refines the five reviewed findings. No learning-log authorship or student
  evaluation claims are included.
