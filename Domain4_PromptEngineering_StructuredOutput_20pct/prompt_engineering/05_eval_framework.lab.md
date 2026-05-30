# Lab guide — `05_eval_framework.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`05_eval_framework.py`](05_eval_framework.py)
> Domain 4 — Prompt engineering (part of the 20% Prompt/Output domain).

---

## What this script does

Compares FOUR prompt versions on the same 10 test cases and prints an accuracy matrix.

## Why we do this (story time)

Like running the same kid through 4 different paths in a maze and seeing which path finishes fastest. You can't tell from one run — you need a real bake-off.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/05_eval_framework.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Loads 10 ticket inputs + expected labels. Runs each of 4 prompt versions through Claude. Builds a table: prompt × case. Prints accuracy per prompt + the failures.

## Try this (a tiny experiment)

Add a 5th prompt that you think is best. Run the eval. If it's not actually better on accuracy + latency, DON'T ship it. That gate is the whole point.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
