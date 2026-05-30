# Lab guide — `02_multi_turn.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`02_multi_turn.py`](02_multi_turn.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Has a back-and-forth conversation by sending the WHOLE chat history every turn.

## Why we do this (story time)

Imagine you only remember things if someone reads your diary to you each morning. Claude is like that — the API is stateless, so we reread the chat every call.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/02_multi_turn.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We build a `messages=[]` list, append the user turn AND the assistant reply each round. Claude 'remembers' previous turns because we keep handing them back.

## Try this (a tiny experiment)

Drop the assistant turns from the list and send only user turns. Claude loses the thread. That single line of code is the difference between a chatbot and a goldfish.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
