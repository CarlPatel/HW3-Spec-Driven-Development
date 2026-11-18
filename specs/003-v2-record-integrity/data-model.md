# V2 data model

V1 entities retained. Event adds previousEventId, sourceDecisions[] and repeat links
as derived classifications. First good part ends the active stop, not closeout.
SourceDecision: source, applicable (boolean), reason, user, at; append-only. Latest
per source applies, default true. Exclusion forbidden if any lock history exists.
Lock evidence remains per cycle, including verification stamps after removal.
Acknowledgment adds isolationFingerprint to existing dated-shift/lock snapshots.
VerificationEvidence: derived candidate shift, completion boundary, blocking stops,
unknown classification and matching recurrence. Derived even before closeout; UI
shows Awaiting closeout until closed while still exposing repeat links.
