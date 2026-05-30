# Advanced Architectural Scenarios — Domain 3 — Claude Code Configuration & Workflows (20%)

Sourced from the consolidated 25 cross-domain scenarios.
Only the **1 scenarios tagged for this domain** appear here.

Sketch an architecture answer first, then compare to the solution sketch at the bottom.

---

## Exercises

**E8.** A devops team wants Claude to suggest fixes when a CI pipeline fails. The PR comment must include a patch. Architect.


---
## Solution sketches

**A8.** Workflow not agent. Chain: read failed step log → identify error class → search repo for related code (RAG) → draft patch → emit unified diff. Comment on PR. No write access to repo; humans merge.
