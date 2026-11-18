# V2 tasks

## Setup and specification
- [X] T001 Preserve V1 and Step 4 inputs in versions/v1/ and step4-evaluation/.
- [X] T002 Record approved F-01–F-05 refinements in spec.md, docs/goal-model.md and constitution.
- [X] T003 Generate plan.md, data-model.md and contracts/ui.md before implementation.
## US1 — Complete isolation records (F-01/F-02)
- [X] T004 [US1] Add source applicability and historical evidence gates in frontend/domain.js (REQ-02/06/09).
- [X] T005 [US1] Expose missing evidence and source decisions in frontend/app.js (REQ-06/09).
## US2 — Preserve separate stop intervals (F-03)
- [X] T006 [US2] Add active-stop and pending-closeout selectors in frontend/domain.js (REQ-01/02/08).
- [X] T007 [US2] Add pending closeout navigation in frontend/app.js (REQ-01/05).
## US3 — Explicit shift acceptance (F-04)
- [X] T008 [US3] Keep dated acknowledgment obligations across notes and critical changes in frontend/domain.js (REQ-07).
## US4 — Evidence-based verification (F-05)
- [X] T009 [US4] Add operating-shift evidence and repeat classification in frontend/domain.js and app.js (REQ-08).
## Validation and preservation
- [X] T010 Add revised regression checks in tests/domain.test.js for all findings.
- [X] T011 Package both frozen V1 and V2 with scripts/build.mjs and Pages workflow.
- [X] T012 Record technical validation and mappings in docs/v2-change-map.md and quickstart.md; preserve local v2 branch.

Dependency order: T001–003 → domain → UI → tests/dual packaging → delivery.
Only independent documentation/layout work could run in parallel; one agent executes.
