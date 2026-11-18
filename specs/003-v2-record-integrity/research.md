# V2 design decisions

Retain existing static architecture to compare requirements changes without backend
changes. Retain client-only state and reason-code proxy with explicit limitations.
Use actual stop/good-part intervals for full-shift evidence; avoid inferring operation
from clock time alone. Preserve removed invalid locks rather than invent backfilled
verification. Keep stamped supervisor source decisions rather than silently dropping
sources. Preserve exact V1 app bytes inside the dual-version Pages artifact.
No new software dependency or external integration is introduced.
