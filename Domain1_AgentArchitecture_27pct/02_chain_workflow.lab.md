# Lab guide — `02_chain_workflow.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`02_chain_workflow.py`](02_chain_workflow.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

It takes a meeting transcript and turns it into a clean to-do list, step by step.

## Why we do this (story time)

Imagine cleaning your room: first you pick up the toys, THEN you put them in the box, THEN you label the box. You can't label before you pick up. A chain workflow does steps in order — each step uses what the last one made.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/02_chain_workflow.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

First Claude pulls action items out of the meeting words. Then it rewrites each one to be specific (who? what? by when?). Then it formats them as a tidy markdown checklist that you can copy into Jira.

## Try this (a tiny experiment)

Delete the middle step (the SMART rewrite) and run again. The checklist is still produced — but the items are fuzzy. That shows why each step in the chain matters.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
