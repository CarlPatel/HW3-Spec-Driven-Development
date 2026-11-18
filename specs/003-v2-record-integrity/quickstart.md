# V2 run and acceptance walkthrough

Node 20+; no install. `npm test`, `npm run build`, `npm start`.
Open http://localhost:4183/ to choose frozen V1 or V2. Both are independent memory-only
mock apps. Reset/reload restores demo records; no push or deployment is performed.

1. F-01: Press 6, Report stop, apply Electrical, record removal without verification.
   Switch supervisor: release lists the retained missing verification. Reset after
   this intentionally incomplete record; no retrospective correction is provided.
2. F-01 valid path: Press 12 has Hydraulic verified. Electrical is applicable by
   default: record/verify/remove it, or switch supervisor and exclude the untouched
   source with a reason. Technician removal and supervisor release now need every
   historical field; applicable sources cannot be silently omitted.
3. F-02: release a complete LOTO record at a later demo time. Operator first good
   part before that release must fail; equal/later time succeeds.
4. F-03: Press 17, stop, advance +15 min, operator good part. Leave code/closeout
   pending. Simulate another stop: a new event runs, the first retains 15 min and
   appears in Pending closeout. Select/code/close it without hiding the active stop.
5. F-04: Molder 8, advance from 06:10 to 06:40. As Maya, add a note. It stays Not
   acknowledged. Acknowledge explicitly to clear it. Critical isolation changes
   invalidate the acknowledgment snapshot; a note alone does not.
6. F-05: close a coded repair after good part. Start an unrelated stop before its
   qualifying full shift, code it differently, leave it stopped and advance beyond
   the shift: the earlier repair is not Verified. Resume the unrelated stop and
   advance through the next full shift: verification becomes supported. Same-code
   recurrence reopens instead; unknown codes keep classification pending.

Domain tests include these scenarios plus exact boundaries, multiple intervals,
retained user identities, role denials and unchanged capture/closure/note behavior.
Build validates frozen V1 checksums. Pages artifact contains only comparison and
application assets; real participant SC-004/005 and stakeholder policy remain unverified.
