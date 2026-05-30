# Lab guide — `05_structured_output.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`05_structured_output.py`](05_structured_output.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Forces Claude to reply in a strict JSON shape so your code can read it.

## Why we do this (story time)

Imagine asking a friend for their address. 'It's somewhere on Main Street, kinda near the park' is useless. A FORM with boxes for street/city/zip is what your computer needs.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/05_structured_output.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We define a tool with an `input_schema` (the form). We use `tool_choice={'type':'tool', 'name':...}` to FORCE Claude to fill the form. The result parses with `json.loads`.

## Try this (a tiny experiment)

Add a new required field to the schema. Re-run. Claude will fill it. If you forgot to give Claude info for the field, watch it make something up — schemas don't validate truth.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
