# Lab guide — `02_few_shot.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`02_few_shot.py`](02_few_shot.py)
> Domain 4 — Prompt engineering (part of the 20% Prompt/Output domain).

---

## What this script does

Shows Claude a few EXAMPLES of input → output so it copies the pattern.

## Why we do this (story time)

Like showing a kid one or two finished colouring pages before handing them a blank one. They copy the style. No examples = total chaos.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/02_few_shot.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We give Claude 3 sample tickets and their labels. Then we ask it to label a NEW ticket. The output matches the example format.

## Try this (a tiny experiment)

Add an example that contradicts the others (deliberately wrong). Watch Claude follow the bad example. Bad examples are louder than instructions — pick yours carefully.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
