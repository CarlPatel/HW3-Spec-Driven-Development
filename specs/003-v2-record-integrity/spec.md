# V2 Specification — Maintenance record integrity

Date: 2026-11-18. Baseline: V1 `bef8e6c`; REQ-01–09 and its 15 goals remain.
Inputs: root traceability.md (user supplied), step4-evaluation/findings.md F-01–F-05,
and the preserved 002 V1 specification. This specification supersedes conflicting
V1 lifecycle/verification clauses for V2 only. V1 is unchanged.

## Approved scope and assumptions

The user approved all five findings, on 2026-11-18, and these mock defaults:
all energy sources apply unless a supervisor excludes a source with a reason;
verification identity/time remains required after removal; production time must
follow release; acknowledgment is explicit per incoming shift; verification needs
a full recorded operating shift. These are team-approved prototype assumptions,
NOT stakeholder-confirmed operating or safety policy. Real policies still need Rob,
Angela and Teo's review. No real physical control/authentication/backend is added.

## Requirements revisions and traceability

| Finding | Revised requirements | Goal | Interview evidence |
|---|---|---|---|
| F-01 | REQ-06/09, FR-012–014/020; FR-021–022 below | G2.1, G2.1.1, G3.4 | T3-L14, T6-L64/L81/L98/L111 |
| F-02 | REQ-02/06, FR-005/015; FR-023 | G1.1.3, G2.1.1 | T2-L9/L14, T11-L14/L22 |
| F-03 | REQ-01/02/08, FR-003/018–019; FR-024 | G1.1, G1.1.1, G1.1.3, G1.9 | T2-L14/L16/L63/L80 |
| F-04 | REQ-07, FR-016–017; FR-025 | G1.3.5 | T1-L47, T10-L11, T11-L22 |
| F-05 | REQ-08, FR-018–019; FR-026–027 | G1.9 | T1-L34/L90, T9-L22 |

All unchanged V1 requirements remain in force. The source/prototype is client-only,
resets on reload, keeps selectable demo identities, and retains the fixed reason list.

- **FR-021 (REQ-06/09)**: Once LOTO is used, every machine energy source defaults to
  Applicable. Only a Shift Supervisor may mark a source Not applicable, with a
  nonempty reason, identity and time. A source with any recorded lock cannot be
  excluded to hide incomplete evidence. Decisions are retained in the timeline.
  Applying a lock never requires a prior applicability form, note or reason code.
- **FR-022 (REQ-06/09)**: Release and closure must enumerate missing applicable
  source records and every recorded lock's missing zero-energy verification,
  verifier identity/time, applier/time, remover/time or invalid chronology, even
  after removal. Each recorded cycle requires its own evidence. Handover permits
  verified active locks, but requires applicable source records and verification
  evidence; it does not require removal or release. Removal may be recorded without
  verification to preserve what actually happened, but must not erase that omission.
  No retrospective verification or silent correction is supported: a removed
  unverified lock remains an incomplete record that blocks release/closeout.
- **FR-023 (REQ-02/06)**: Good-part time must be finite, at/after stop, not future,
  and for LOTO at/after the latest valid release and all recorded removals. It must
  not fall inside an isolation interval. Stop ≤ apply ≤ verify ≤ remove ≤ release
  ≤ first good part; equal times are allowed. Out-of-order times are refused and
  explained. Timestamps are automatically captured at demo clock time except the
  operator's first-good-part input; reviewed corrections remain out of scope.
- **FR-024 (REQ-01/02/08)**: At most one ACTIVE STOP interval per machine, defined
  by absent first good part. Further signals during that interval deduplicate.
  After first good part a new stop creates a separate interval even if older records
  await reason or closure. Older durations/evidence remain intact and selectable in
  Pending closeout; the new event links to its predecessor. Closure of an older
  record must not hide the current active stop. A first-good-part record precedes opening the next stop interval; later correction
  of first-good-part timestamps is unsupported, preventing overlapping intervals.
- **FR-025 (REQ-07)**: Each unclosed event that predates the current dated shift
  start owes explicit acknowledgment for that shift, overdue exactly 30 minutes in.
  Notes, removal, verification and reason edits never clear that obligation. Current
  shift technician/supervisor may acknowledge; operator may not. New/changed critical
  isolation information after acknowledgment requires reacknowledgment, while the
  earlier acknowledgment snapshot remains. Critical information means lock apply,
  verification/removal, or source applicability decision. Notes do not invalidate it.
- **FR-026 (REQ-08)**: A closed repair is Verified only when the recorded machine
  operation covers an entire calendar shift starting at/after its first good part,
  without a new stop in that shift. A different-category stop interrupts operating
  evidence: wait for its first good part, then the next complete shift. Do not claim
  full operation while a recorded stop overlaps that shift. This is recorded demo
  evidence, not sensor proof or stakeholder validation.
- **FR-027 (REQ-08)**: Before the first qualifying operating shift finishes, a
  later stop with the same fixed-list reason reopens the prior repair and links both
  records, regardless of delayed administrative closure. Unknown reasons keep the
  prior repair Awaiting evidence, even when coded after the candidate deadline.
  A different reason is not a matching repeat but can interrupt operation. Matching
  by reason remains an explicit, unresolved proxy for actual fault identity. A stop
  exactly at a completed qualifying shift's end does not invalidate that shift.
  Display Awaiting closeout, Awaiting evidence, No matching recurrence observed —
  awaiting a full operating shift, Reopened — repeat fault, or Verified — recorded
  full [shift] as warranted; do not equate no matching code with verified repair.

## Acceptance scenarios

1. F-01: Given an unverified Electrical lock, when it is removed, release and close
   list its missing verification. Historical omission remains visible; no backfill.
2. F-01: Given only Hydraulic recorded on a two-source press, release/handover list
   missing Electrical. A supervisor can exclude the never-locked Electrical source
   with a reason; a technician cannot. Verified active applicable locks can hand over.
3. F-02: Given removal/release at 14:00, first good part at 12:00 is refused; 14:00
   succeeds. Earlier-than-stop/future checks remain. A fresh lock invalidates release.
4. F-03: Given stop 06:55 and good part 07:10 with no reason, a stop 07:25 creates a
   new running interval. The first remains 15 minutes in Pending closeout; another
   stop signal deduplicates the new interval. Closing the first leaves the new active.
5. F-04: Given overdue handover at 06:30, a current-shift note leaves it overdue with
   zero acknowledgments. Explicit acknowledgment clears it; the next shift owes its
   own acknowledgment. A changed isolation snapshot requires a fresh acknowledgment.
6. F-05: Given good part 06:10, an unrelated 07:00 stop with no later good part cannot
   yield Verified at 22:05. If production resumes at 15:00, the Night shift 22–06 can
   qualify at 06:00 next day. A matching stop before that completion reopens; an
   uncoded stop keeps classification pending. At 06:00 exactly, Day can qualify by 14.
7. Regression: no-field manual/sensor opening, reason-list closure, notes/photo-only
   input, role restrictions, history, auto stamps and unresolved C-2 remain preserved.

## Relationships, conflicts and limits

C-1 and C-4 retained: capture first; require code at closure; notes/photos supplement.
C-2 retained unresolved: one stop-to-good-part clock includes LOTO hold and is flagged.
C-6 retained: source taps, automatic identities/times; completeness gates occur after
capture. F-03 resolves the one-open-record ambiguity by separating active stop from
administrative closeout. F-04 separates acceptance from authorship. I-2 retains two
milestones: production resumption vs. evidence of a durable repair. FR-026 strengthens
the latter without claiming that reason categories uniquely identify faults.
Source applicability, real verifier/remover authority, fault identity, time corrections
and actual operating evidence require stakeholder confirmation. Human SC-004/005 and
the previously blocked browser photo check are not silently marked satisfied.
