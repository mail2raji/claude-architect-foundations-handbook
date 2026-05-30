# Lab guide — `02_multi_turn_tools.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`02_multi_turn_tools.py`](02_multi_turn_tools.py)
> Domain 2 — Tool design (part of the 18% Tool/MCP domain).

---

## What this script does

Shows the FULL agent loop: keep going around (assistant → tool → assistant → tool …) until Claude says 'I'm done'.

## Why we do this (story time)

Like a scavenger hunt: every clue tells you where to look next, until the last clue says 'you win!'. You don't stop after one clue — you stop when the game ends.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/tool_use/02_multi_turn_tools.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Claude asks for tool A, we run it, tool A's result triggers tool B, we run B, then Claude has enough to write the final answer (stop_reason='end_turn').

## Try this (a tiny experiment)

Set max_steps=1. Now the loop ends after one tool call even though Claude isn't finished. That's why max_steps is a SAFETY knob, not just a debug knob.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
