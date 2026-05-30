# Lab guide — `01_first_message.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`01_first_message.py`](01_first_message.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Walks through the four fields every Claude call needs: model, max_tokens, system, messages.

## Why we do this (story time)

Like the four corners of a sandwich: top bread (system), bottom bread (max_tokens cap), filling (messages), and the label that says 'tuna' (model). Miss one and the sandwich falls apart.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/01_first_message.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We send one message, print the reply, AND print the stop_reason so you see what 'end_turn' looks like in practice.

## Try this (a tiny experiment)

Set max_tokens=5. Watch stop_reason flip to 'max_tokens' — the reply is cut off mid-sentence. That's the cap doing its job.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
