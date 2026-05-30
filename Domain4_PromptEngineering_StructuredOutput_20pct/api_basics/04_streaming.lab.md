# Lab guide — `04_streaming.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`04_streaming.py`](04_streaming.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Prints Claude's reply as it 'types' instead of waiting for the whole answer.

## Why we do this (story time)

Like watching a friend write — words appear one by one. You start reading sooner, even though the total time is the same.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/04_streaming.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We use `client.messages.stream(...)` and print each text delta. The reply trickles to your terminal token by token.

## Try this (a tiny experiment)

Time the FIRST printed character vs total time. The first character lands almost immediately — that's the UX win streaming gives chat apps.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
