# Lab guide — `05_builtin_web_search.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`05_builtin_web_search.py`](05_builtin_web_search.py)
> Domain 2 — Tool design (part of the 18% Tool/MCP domain).

---

## What this script does

Uses Anthropic's built-in web_search tool — Claude does the search itself, you don't have to run anything.

## Why we do this (story time)

Like a magic answering machine that already knows how to Google. You just give it the question; it does the search and reads the page for you.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/tool_use/05_builtin_web_search.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We pass `tools=[{'type': 'web_search_20250305', ...}]` and ask a current-news question. Claude returns text WITH source citations attached.

## Try this (a tiny experiment)

Ask a question that can't be answered from the web (e.g. 'what did Bob email me yesterday?'). Watch Claude refuse or say it can't find it. That's the boundary of built-in tools — they only see public info.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
