# Lab guide — `04_code_review_agent.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`04_code_review_agent.py`](04_code_review_agent.py)
> Domain 3 — Claude Code workflows (20% of the exam).

---

## What this script does

Reads a code change and writes review comments — like a careful friend looking over your homework before you turn it in.

## Why we do this (story time)

Teacher checks your spelling, math, and neatness in three passes. Each pass spots different mistakes. One big 'check everything' pass would miss stuff.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain3_ClaudeCode_Workflows_20pct/capstones/04_code_review_agent.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Multi-pass review: pass 1 = correctness, pass 2 = security, pass 3 = tests. Each pass uses a TIGHT prompt with explicit criteria, then the findings are merged.

## Try this (a tiny experiment)

Try ONE pass with vague 'review this code' vs THREE passes with explicit rubrics. The 3-pass version catches ~2× more real issues for ~2× the cost — usually worth it.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
