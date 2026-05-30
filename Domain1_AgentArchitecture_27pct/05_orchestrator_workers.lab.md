# Lab guide — `05_orchestrator_workers.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`05_orchestrator_workers.py`](05_orchestrator_workers.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

One 'boss' Claude breaks a big task into small pieces, then sends each piece to a 'worker' Claude.

## Why we do this (story time)

Building a Lego castle: dad draws the plan (orchestrator), the kids each build a tower (workers), then dad glues them together. Faster than dad building alone.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/05_orchestrator_workers.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

The boss reads a big research question and writes 3 sub-questions. Each sub-question is answered by a worker in parallel. The boss reads all 3 answers and writes the final brief.

## Try this (a tiny experiment)

Print the orchestrator's plan before workers run. You'll see how Claude actually decomposes a problem, which is the most exam-relevant skill.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
