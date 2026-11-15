# Design decisions

- Decision: native browser modules and Node built-ins. Rationale: six-machine mock
  prototype needs no framework or network packages. Alternative: React/Vite adds
  dependencies without changing requirement coverage.
- Decision: one domain module owns all validations; role changes are demo context.
  Rationale: buttons alone must not enforce gates. Alternative: UI-only guards
  permit inconsistent transitions.
- Decision: local calendar shift boundaries (06/14/22), immutable timestamped records,
  and a forward-only demo clock. Alternative: real timers make boundary tests slow.
- Decision: repeat detection uses event stop time, not the later reason-entry time.
  An uncoded stop inside a verification window delays verification until coded;
  then the earlier event is reopened only for a matching reason. This explicitly
  resolves the implementation sequencing gap without requiring a reason at opening.
- Decision: small raster photo attachment via browser FileReader, held in memory;
  unsupported/non-image or >5 MiB files are refused as a prototype assumption.
- All stakeholder confirmation markers and C-2 in the spec remain unresolved.
