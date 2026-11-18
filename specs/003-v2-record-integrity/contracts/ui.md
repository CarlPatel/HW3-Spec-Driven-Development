# V2 UI/domain contract

activeFor(s,machine): only event without first good part. openRecords(s,machine): all
unclosed events; openFor prioritizes active then newest pending closeout.
isolationMissing(s,e,phase): enumerates missing applicable sources, historical lock
identity/time/verification and chronology; release also needs all removals.
setSourceApplicable: supervisor-only, nonempty exclusion reason, no lock history.
handover: closed records excluded; otherwise dated obligation independent of notes.
verificationEvidence: full operating-shift scan; unknown reason holds classification.
UI: machine list, independent Pending closeout records, active-stop selector, source
applicability form, historical lock evidence, phase-specific missing messages,
verification evidence and retained stamps. Validation errors remain readable.
