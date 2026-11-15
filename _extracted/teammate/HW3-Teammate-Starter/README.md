# HW3 teammate starter packet

Prepared November 14, 2026 from existing local course caches and relevant prior chats; Canvas was not rechecked today.

## Start here

1. Read `assignment/17626 HW 3 Spec-Driven Development.pdf` (the current handout in the local cache).
2. Open `assignment-2/review/diagrams.html` for Timothy's three stakeholder goal models and combined model; `review.html` shows the catalog and use cases. Keep the vendor folder alongside diagrams.html.
3. Review `assignment-2/submission/goal_model_*.py`, `goal_catalog.py`, `generated/`, `use_cases.json`, and `matrix.json`. Keep the support files and `goalmodeling/` together. From that submission folder, `python3 goal_model_combined.py` runs the combined model (Python 3.10.5+).
4. Use `stakeholder-interviews/*.csv` and `assignment-2/review/goal_evidence.csv` to trace claims to stakeholder passages and timestamps. `use_case_evidence.json` supplies use-case provenance. These Assignment 2 matrices are inputs; HW3 requires a new matrix extending through specification IDs, implementation, and satisfaction status.
5. Review `assignment-2/review/analysis.md` for conditional conflicts, merged IDs, and assumptions. Yellow nodes/marked text are analyst interpretations requiring review. `glossary.md` and `glossary-entries.json` provide earlier terminology.
6. Each teammate should share their own Assignment 2 models and any additional interview evidence. Merge the team's findings, then choose a coherent subset of core, user-facing, or uncertain goals.

## Coordinate as a team

- Agree on selected goals, scope, priorities, overlaps, dependencies, conflicts, and assumptions.
- Create a private GitHub repository and give teammates access; set up GitHub Spec Kit and an AI development tool.
- Assign responsibilities for model/spec work, implementation, evaluation/traceability, deployment, and final checks; record everyone's contributions.
- Preserve the V1 goal model, spec, Spec Kit artifacts, and source; deploy V1.
- Evaluate V1 against stakeholder evidence and requirements. Distinguish implementation defects from requirements issues.
- Revise the spec and goal model before changing intended behavior. Preserve V2 in the same repository and deploy it separately. Show at least one meaningful requirements-level improvement discovered through V1 evaluation.
- Team members must author `learning-log.md` themselves: the handout prohibits AI assistance with authorship and Step 6 examples/answers. This packet contains no HW3 learning-log draft.

## Final submission checklist

Submit one GitHub repository URL through Canvas for the existing assigned group. The default README must link directly to V1 code, V2 code, deployed V1, deployed V2, and the Requirements Analysis and Learning Log document. Include a Roles and Responsibilities section. The repository must contain source, goal models, Spec Kit artifacts, traceability matrix, and learning document. Both deployments must remain accessible for evaluation.

Cached deadline: Wednesday, November 18, 2026, 10 p.m. America/New_York (Eastern), verified on the assignment page November 9 and in Canvas Grades November 11. This is cached verification, not a live check on November 14.

## Sources and provenance

- Submission page: https://canvas.cmu.edu/courses/56785/assignments/1038199
- Updated handout: https://canvas.cmu.edu/courses/56785/files/15145056?wrap=1
- Announcement: https://canvas.cmu.edu/courses/56785/discussion_topics/872533
- Handout downloaded November 8; cached/extracted November 9. Older email file ID 15144934 was superseded by the live link to 15145056.
- Assignment 2 artifacts were prepared November 4–5 with AI assistance documented in `assignment-2/submission/AI_ASSISTANCE.md`; review them against the evidence before adopting them.
- Five locally saved Clarity CSVs: Teo initial and two follow-ups, Angela initial, and Rob interview. No Angela follow-up CSV is in this cache. Ask teammates for additional evidence.
- Only team-relevant Assignment 2 artifacts are included; individual reflection PDFs are omitted.
- Required Spec Kit readings from the handout: https://github.github.io/spec-kit/quickstart.html and https://github.github.io/spec-kit/reference/agentic-sdd.html (not fetched today).
