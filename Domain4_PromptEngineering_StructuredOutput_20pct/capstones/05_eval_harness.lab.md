# Lab guide — `05_eval_harness.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`05_eval_harness.py`](05_eval_harness.py)
> Domain 4 — Prompt engineering (part of the 20% Prompt/Output domain).

---

## What this script does

A mini test-suite for prompts — runs your prompt against a list of cases and tells you the score.

## Why we do this (story time)

Like a spelling-test grader: same 20 words every week, you see if your kid is improving. Without the test you can't tell if a change helped.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/capstones/05_eval_harness.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Loads a small JSON of test cases ({input, expected}). Runs your prompt on each. Prints accuracy + average latency. Saves results to a file you can diff next time.

## Try this (a tiny experiment)

Run it BEFORE and AFTER changing your prompt. The diff in scores tells you whether your 'improvement' is real or imagined. This single tool is the #1 production discipline.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
