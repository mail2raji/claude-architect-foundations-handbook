# Lab guide — `04_prefilling.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`04_prefilling.py`](04_prefilling.py)
> Domain 4 — Prompt engineering (part of the 20% Prompt/Output domain).

---

## What this script does

Starts Claude's reply FOR it (e.g. with `{`) so it's forced to continue in the format you want.

## Why we do this (story time)

Like handing your kid the crayon already on the page — they can only finish the picture, they can't start somewhere else.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/04_prefilling.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We add an assistant turn with `content='{'`. Claude has to continue with valid JSON or it'll look silly. Three demos: force JSON, force a numbered list, force a fenced code block.

## Try this (a tiny experiment)

Remove the prefill but add 'respond with JSON' in the instruction. Watch Claude sometimes prepend 'Sure, here is the JSON:' — prefill prevents that 100%.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
