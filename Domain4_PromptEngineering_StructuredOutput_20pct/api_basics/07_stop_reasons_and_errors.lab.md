# Lab guide — `07_stop_reasons_and_errors.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`07_stop_reasons_and_errors.py`](07_stop_reasons_and_errors.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Demos every `stop_reason` Claude can return — and what each one means you should do next.

## Why we do this (story time)

Traffic-light vocabulary: green = drive, yellow = slow, red = stop, flashing red = something's broken. Each stop_reason is a different colour.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/07_stop_reasons_and_errors.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We trigger end_turn (normal), max_tokens (raise the cap), stop_sequence (you told it to stop on a word), and tool_use (Claude wants a tool). Each is printed with the right next-step.

## Try this (a tiny experiment)

Wrap each call in try/except and trigger a rate-limit error on purpose (loop with no sleep). See the retry/backoff message format — exam favourite.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
