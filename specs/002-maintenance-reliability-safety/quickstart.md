# Run and validate V1

From repository root with Node 20+: `npm test`, `npm run build`, `npm start`.
Open http://localhost:4173. No install or secrets required. Reload resets mock data.

1. Report stop on Old Blue in one tap from list; confirm no sensor warning.
2. Simulate Press 17 stop twice; one event remains. Switch to operator, confirm
   first good part; close as technician without a reason to see missing fields.
3. Apply Hydraulic/Electrical locks as technician. Operator's good-part action
   must fail. Remove each lock, switch supervisor, authorize; operator can resume.
4. Add a short next action or photo on Molder 8. Switch incoming technician,
   acknowledge; remove zero-energy verification from the workflow by leaving a
   fresh lock unverified and observe acknowledgment refusal instead.
5. Advance clock through 06:30 to see unacknowledged previous-shift repairs highlighted.
6. Close a coded repair; advance through the next full shift to verify it. In a
   fresh demo, create a matching stop before that deadline, code it, and inspect
   the linked reopened repair. A different reason must not reopen it.

Automated rule checks: `npm test`. Human comprehension/timing criteria SC-004/005
still need student evaluation; automated checks do not establish stakeholder satisfaction.
