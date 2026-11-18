# Step 4 — V1 evaluation package

Technical evaluation prepared November 15, 2026 for the team’s review.

- **[Requirements traceability matrix](traceability.md)** and [CSV](traceability.csv): all nine requirements, interview evidence, repository goal IDs, implemented functions and satisfaction status.
- **[Five evaluation findings and proposed V2 requirement changes](findings.md)**: each has a classification, observed behavior, stakeholder evidence, proposed revision and retest.
- **[All 20 functional requirements](fr-coverage.csv)**: checked behavior and remaining validation.
- **[Browser evidence index](evidence/README.md)**: 33 rendered-state observations and screenshots (32 completed checks plus one blocked upload attempt).
- **[Verified interview locators](evidence/interview-evidence.csv)**: cited CSV records and UTC timestamps from all relevant source sets.
- **[Remaining direct human/browser checks](human-checks.md)**: SC-004/005 timing/comprehension and the environment-blocked photo browser path.

## Evaluated baseline

- Repository: https://github.com/CarlPatel/HW3-Spec-Driven-Development
- V1 branch at retrieval: `bef8e6c0bfae46af486e561841c32f9c8d159b88`.
- Authoritative spec: [002 maintenance reliability/safety](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/specs/002-maintenance-reliability-safety/spec.md). It contains REQ-01–09, FR-001–020 and 15 selected goals.
- Prototype interacted with: https://carlpatel.github.io/HW3-Spec-Driven-Development/v1/
- Goal model used for traceability: the repository’s hierarchical G#.# model in [docs/goal-model.md](https://github.com/CarlPatel/HW3-Spec-Driven-Development/blob/bef8e6c0bfae46af486e561841c32f9c8d159b88/docs/goal-model.md), including its appended V1 scope alignment. The earlier local 20-goal overview is not silently substituted.
- Local read-only source/evidence cache: `source-snapshot/`. Source URLs/blob identifiers are in its cache manifest. Snapshot files are text obtained through the connected GitHub tools; the source commit is pinned for reproducibility.

The live deployment’s tested behavior was consistent with the inspected V1 source. No cryptographic asset-to-deployment-commit identity was established; browser observations describe the live URL at evaluation time, and deterministic tests describe the pinned source snapshot.

## Results and limits

The 15 existing domain tests passed and the static build succeeded. Thirty-three browser observations include 32 completed UI checks and one environment-blocked upload attempt. Six additional local probes reproduced the five requirements issues. No application implementation or original spec was changed, and the browser demo was reset.

The selected goals are only partly satisfied in several areas despite the existing tests passing. The findings concern incomplete release evidence, inconsistent production/release times, a lost second breakdown before paperwork closure, disappearing handover obligations, and a full-shift verification label unsupported by operating evidence. They are classified against the written requirements in findings.md; a passing test suite does not establish that those requirements are complete.

Human SC-004/005 results are pending. Photo browser selection/display was blocked by extension file-access permission; the open-only/all-machines filters passed. These limits are explicit in the matrix; no student/stakeholder session or production safety validation is claimed.

## Reproduce

In `source-snapshot/`: `npm test` and `npm run build` (Node 20+, no dependency installation).

In this folder: `node reproduce-findings.mjs`.

Cached outputs are in `evidence/existing-test-results.txt`, `evidence/build-results.txt` and `evidence/reproduction-probes.json`. The probe assertions reproduce V1 behavior; they are not approvals of the problematic behavior.

## Next use

The team should review the findings and any remaining direct checks, choose a meaningful requirements-level improvement, then revise the goal model/spec before changing V2 behavior. Preserve V1 unchanged for comparison. This package can be copied into the team repository as technical Step 4 artifacts.

This is AI-assisted technical evaluation, **not `learning-log.md` or a student reflection**. Team members must author the learning log independently, following the handout. No GitHub branch, commit, PR, comment, message or submission was published during this task.

## Assignment cache

Original HW3 handout: parent assignment `materials/17626 HW 3 Spec-Driven Development.pdf`. Canvas submission: https://canvas.cmu.edu/courses/56785/assignments/1038199. Cached deadline: November 18, 2026, 10 p.m. America/New_York, last verified November 11; Canvas was not rechecked today. Final submission is one repository URL with V1/V2 artifacts, both deployment URLs, traceability, the student-authored learning log and roles/contributions linked from the default README.
