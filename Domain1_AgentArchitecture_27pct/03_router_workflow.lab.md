# Lab guide — `03_router_workflow.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`03_router_workflow.py`](03_router_workflow.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

It looks at a message and decides which 'helper' should answer it — billing, technical, or refund.

## Why we do this (story time)

Think of a school nurse who looks at a kid and says 'cut → band-aid, fever → cot, sneeze → tissue'. The nurse doesn't fix anything — she just routes you to the right person.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/03_router_workflow.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

A small, fast model reads the question and picks a label (billing/tech/refund). Then the right specialist prompt runs, and you get the specialist's reply.

## Try this (a tiny experiment)

Send it a weird message that fits TWO categories (e.g. 'I can't log in to pay my bill'). Watch which way it routes.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
