# Data model

Machine: id, name, nickname, asset, line, sensors, energySources; six demo rows.
User: id, name, role, shift (demo identities, not authentication).
State: machines, users, events, now (epoch milliseconds), sequence.
Event: id, machineId, stoppedAt, source, openedBy, openedShift, reason,
firstGoodAt|null, closedAt|null, entries[], locks[], release|null,
acknowledgments[], includedLotoHold, repeatOf|null, reopenedBy|null.
Entry: found, tested, temporary, next, photo|null, user, at, shift.
Lock: id, source, appliedBy, appliedAt, zeroEnergy, removedBy|null, removedAt|null.
Release: user, at; invalidated by each new lock cycle.
Acknowledgment: user, at, shiftStart, locks snapshot (source/applier).

Invariants: one open event per machine; timestamp order; listed reason required
at close; no active lock or missing authorization at good part or close; no
acknowledgment with unverified active lock. Closed records cannot be edited.
Verification is derived from first-good-part's next full calendar shift and later
stops/reasons; link repeat events bidirectionally. No database/API exists.

