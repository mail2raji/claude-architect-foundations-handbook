# Lab guide — `01_function_calling.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`01_function_calling.py`](01_function_calling.py)
> Domain 2 — Tool design (part of the 18% Tool/MCP domain).

---

## What this script does

Teaches Claude to call a Python function (a 'tool') instead of guessing the answer in its head.

## Why we do this (story time)

Imagine you ask a friend 'what's 17 × 23?'. A polite friend says 'one sec' and pulls out a calculator. Tools let Claude do the same — use the right gadget for the job.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/tool_use/01_function_calling.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We define a weather tool. We ask Claude about Sydney's weather. Claude responds NOT with an answer but with a tool-call: 'please call get_weather("Sydney")'. We run the tool, send back the result, then Claude says '22 °C'.

## Try this (a tiny experiment)

Ask 'what's the weather in Atlantis?' (a place the tool doesn't know). Watch how Claude handles the empty/error result. Good error handling is half of tool design.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
