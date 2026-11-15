# Tasks: V1 Maintenance Reliability and Safety

## Phase 1: Setup
- [X] T001 Add dependency-free commands in package.json and scripts/build.mjs, scripts/serve.mjs.
## Phase 2: Foundation
- [X] T002 Define demo machines/users and clock/shift helpers in frontend/domain.js (REQ-01–09).
## Phase 3: US1 (P1) — downtime
Independent test: duplicate stops, 48-minute good part, missing closure fields.
- [X] T003 [US1] Implement event opening, reason, good part and closure in frontend/domain.js (REQ-01–03).
- [X] T004 [US1] Build machine list and event completion controls in frontend/app.js (REQ-01–03).
## Phase 4: US2 (P1) — isolation
Independent test: lock → blocked good part → removal → supervisor release.
- [X] T005 [US2] Implement lock/zero-energy/removal/release guards in frontend/domain.js (REQ-06/09).
- [X] T006 [US2] Build stamped energy-source controls in frontend/app.js (REQ-06/09).
## Phase 5: US3 (P2) — handover
Independent test: note/photo → incoming shift summary → acknowledgment; incomplete lock refusal.
- [X] T007 [US3] Implement entries, summaries and shift acknowledgments in frontend/domain.js (REQ-04/05/07/09).
- [X] T008 [US3] Build note/photo form, open repair list and timeline in frontend/app.js (REQ-04/05/07/09).
## Phase 6: US4 (P3) — verification
Independent test: next full shift verification and same/different reason repeats.
- [X] T009 [US4] Implement verification deadlines and repeat links in frontend/domain.js (REQ-08).
- [X] T010 [US4] Display verification/history and demo clock in frontend/app.js (REQ-08).
## Phase 7: Validation and delivery
- [X] T011 Add acceptance-rule checks in tests/domain.test.js (REQ-01–09).
- [X] T012 Add responsive styles in frontend/styles.css and accessible frontend/index.html (G4).
- [X] T013 Document usage, scope and implementation references in README.md and docs/implementation-map.md.
- [ ] T014 Build/check V1, preserve Git version and deploy; record actual status in docs/v1-delivery.md.

## Dependencies and strategy
T001 → T002 → US1 → US2 → US3 → US4 → validation/delivery.
MVP is US1; V1 includes all four stories. Shared module edits are sequential.
Optional parallel review: UI layout vs. documentation after domain contracts stabilize.

T014 partial: local validation complete; external deployment awaits permission.
