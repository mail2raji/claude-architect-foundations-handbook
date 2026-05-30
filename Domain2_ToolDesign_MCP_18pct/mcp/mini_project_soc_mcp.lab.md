# Lab guide — `mini_project_soc_mcp.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`mini_project_soc_mcp.py`](mini_project_soc_mcp.py)
> Domain 2 — MCP (part of the 18% Tool/MCP domain).

---

## What this script does

A real-shaped MCP server for security analysts: query Sentinel, close incidents, fetch incident JSON.

## Why we do this (story time)

Like turning your toolbox into a USB stick — once it's an MCP server, ANY AI tool can plug in and use your hammer.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/mcp/mini_project_soc_mcp.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Tools: `query_sentinel(kql)`, `close_incident(id, reason)`. Resource: `sentinel://incident/{id}` returns JSON. Prompt: `/triage-incident severity=high` injects a ready-made prompt.

## Try this (a tiny experiment)

Wire this server into Claude Desktop config. Ask 'show me yesterday's high-severity incidents'. Claude calls your tool through MCP without you writing any client code.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
