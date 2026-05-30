# Lab guide — `06_evaluator_optimizer.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`06_evaluator_optimizer.py`](06_evaluator_optimizer.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

Claude writes something, then a SECOND Claude grades it. If the grade is too low, it tries again.

## Why we do this (story time)

Like a kid drawing a picture, showing it to mom, mom says 'add a sun', kid adds a sun, shows again, mom says 'perfect'. Loop until perfect (or until you run out of crayons).

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/06_evaluator_optimizer.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

Claude drafts a customer-support reply. A judge Claude scores it 1–5 against a rubric. If <4, the draft is rewritten with the judge's feedback. After 3 tries it stops.

## Try this (a tiny experiment)

Make the rubric impossible (e.g. require 'use exactly 17 emojis'). Watch the loop hit max-rounds and stop without converging — that's the EARLY-STOP knob saving you money.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
