# Lab guide — `00_setup_first_call.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`00_setup_first_call.py`](00_setup_first_call.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Your VERY first Claude call — proves your API key works and Python can reach Anthropic.

## Why we do this (story time)

Like flipping the light switch the first day you move in. Before you decorate the room, you check the lights actually work.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/00_setup_first_call.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Loads your `.env`, calls `client.messages.create(...)` with a tiny prompt, prints the reply. If you see Claude's text, you're good.

## Try this (a tiny experiment)

Run it without setting ANTHROPIC_API_KEY. Read the error. Now you know what 'no auth' looks like — useful when you debug coworkers.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
