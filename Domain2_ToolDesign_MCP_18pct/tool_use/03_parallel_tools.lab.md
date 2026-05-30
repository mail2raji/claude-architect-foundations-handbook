# Lab guide — `03_parallel_tools.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`03_parallel_tools.py`](03_parallel_tools.py)
> Domain 2 — Tool design (part of the 18% Tool/MCP domain).

---

## What this script does

Shows Claude asking for THREE tools in the same turn so they run side by side instead of one at a time.

## Why we do this (story time)

Like ordering pizza AND fries AND soda all at once — much faster than 3 separate trips. Parallel tool use trims latency a LOT.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/tool_use/03_parallel_tools.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Claude returns three tool_use blocks in one assistant message. We run all three (in threads), bundle their results, and send back ONE user turn with three tool_result blocks.

## Try this (a tiny experiment)

Time the script with parallel vs sequential execution (use a stopwatch). The speedup is visible even on tiny tools.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
