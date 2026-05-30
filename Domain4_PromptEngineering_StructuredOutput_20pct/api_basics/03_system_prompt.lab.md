# Lab guide — `03_system_prompt.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`03_system_prompt.py`](03_system_prompt.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Shows the `system` field — the instructions that stay TRUE for every turn (tone, persona, rules).

## Why we do this (story time)

Like the rules taped to the fridge: 'no running, no shouting, ask before snacks'. They don't change when grandma visits — they apply to every conversation in the house.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/03_system_prompt.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We send the same question with three different system prompts (terse / friendly / pirate). Same model, same user message — the only thing that changes is tone.

## Try this (a tiny experiment)

Move the rules into the user message instead of `system`. They still work but Claude trusts them less. System is the SAFEST place for persistent rules.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
