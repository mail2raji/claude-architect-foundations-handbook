# Advanced Architectural Scenarios — Domain 4b — Prompt Engineering & Evaluation (part of Domain 4, 20%)

Sourced from the consolidated 25 cross-domain scenarios.
Only the **1 scenarios tagged for this domain** appear here.

Sketch an architecture answer first, then compare to the solution sketch at the bottom.

---

## Exercises

**E24.** Design an eval suite to detect regressions when Anthropic changes a model snapshot.


---
## Solution sketches

**A24.** Per-prompt golden datasets (100+ cases each). Run nightly across model snapshots. Track accuracy, calibration, token counts, latency. Alert on >2% drop or >20% token drift. Use LLM-judge (Opus) for open-ended; exact match for classification.
