# Lab guide — `03_chain_of_thought.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`03_chain_of_thought.py`](03_chain_of_thought.py)
> Domain 4 — Prompt engineering (part of the 20% Prompt/Output domain).

---

## What this script does

Tells Claude to 'think out loud' inside a `<thinking>` block before giving the final answer.

## Why we do this (story time)

Like showing your work in maths. The teacher (and Claude) both make fewer mistakes when the steps are written down instead of done in their head.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/03_chain_of_thought.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We ask a multi-step word problem two ways: direct vs with `<thinking>`. The thinking version usually gets the right answer and we strip the thinking out for the user.

## Try this (a tiny experiment)

Hide the thinking from the user but log it. That's the 'extended thinking' pattern Claude uses internally — invisible but valuable for debugging.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
