# Lab guide — `01_xml_tags.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`01_xml_tags.py`](01_xml_tags.py)
> Domain 4 — Prompt engineering (part of the 20% Prompt/Output domain).

---

## What this script does

Wraps parts of your prompt in `<tags>` so Claude knows which bit is data vs which bit is instruction.

## Why we do this (story time)

Imagine giving someone a shopping list AND a recipe in one note. If you put a box around each, no one is confused. XML tags are those boxes.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/01_xml_tags.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Same task run two ways: messy text vs neatly tagged. The tagged version gets more accurate output because Claude can see 'this is the user comment, this is the rule'.

## Try this (a tiny experiment)

Strip the tags but keep the same words. The output gets sloppier. That delta is the whole reason Anthropic recommends XML tags.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
