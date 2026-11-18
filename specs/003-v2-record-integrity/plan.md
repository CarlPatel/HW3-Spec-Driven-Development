# V2 implementation plan

Date 2026-11-18; branch v2; input spec.md; baseline bef8e6c.

## Technical context
Retain dependency-free browser JavaScript/HTML/CSS and Node 20+ checks. Memory-only
mock state; no new runtime packages. One domain module guards transitions; UI
exposes records, missing fields, applicability and separate closeout/active stops.

## Constitution gate
PASS: revised spec precedes behavior; REQ/goal/evidence links preserved; mock-only;
no blocking form before capture; safety evidence checked at handover/release/close;
C-2 and unconfirmed stakeholder policy remain explicit. Recheck after implementation.

## Design
F-01: source decisions[], complete historical lock validator with phase-specific gates.
F-02: production chronology checked against release/removal and subsequent stops.
F-03: activeFor vs openRecords selectors; predecessor links; pending closeout UI.
F-04: obligation from stoppedAt < dated shift start; acknowledgment stores critical
isolation fingerprint, leaving prior snapshots intact; notes don't affect obligation.
F-05: chronological operating-window scan to find first fully uninterrupted eligible
shift; all earlier unknown/matching stops affect classification, independent of closure.

## Structure and validation
frontend/domain.js, app.js, styles.css; tests/domain.test.js rewritten for revised
acceptance criteria and retained nominal behavior. versions/v1/frontend is frozen;
scripts/build.mjs verifies it against baseline, builds dist/v1 and dist/v2 plus
comparison index. serve.mjs serves built comparison. Pages packages both versions.
Keep supplied traceability immutable; add docs/v2-change-map.md and validation facts
without student reflections or learning-log answers. No push/deploy per user preference.

## Workflow provenance
Use existing Spec Kit artifact format and plan → tasks → implement order. No
PowerShell/slash-command runner is available; direct artifact generation is disclosed.
No extension hooks or 003 review checklists are registered. No research delegation needed.
