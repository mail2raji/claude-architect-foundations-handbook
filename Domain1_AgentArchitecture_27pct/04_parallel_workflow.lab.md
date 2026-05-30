# Lab guide — `04_parallel_workflow.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`04_parallel_workflow.py`](04_parallel_workflow.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

It runs the same task five times at once and lets a 'voter' pick the best answer.

## Why we do this (story time)

Imagine asking 5 grandmas the same cookie question. Most will agree. You trust the answer that the most grandmas gave. That's voting — safer than asking just one.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/04_parallel_workflow.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

Five copies of Claude classify the same ticket. Their votes are counted. The majority wins. You see the per-voter labels and the final winner.

## Try this (a tiny experiment)

Set the temperature to 0 for every voter and re-run. Now they all give the SAME answer, so voting adds nothing. That shows when voting helps and when it's wasted money.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
