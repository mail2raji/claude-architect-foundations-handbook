# Lab guide — `03_mcp_client.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`03_mcp_client.py`](03_mcp_client.py)
> Domain 2 — MCP (part of the 18% Tool/MCP domain).

---

## What this script does

Talks TO an MCP server the way Claude Desktop does — opens a session, lists tools, calls one.

## Why we do this (story time)

Like a kid walking up to a lemonade stand: 'what flavors do you have?' (list_tools), then 'one strawberry please' (call_tool).

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/mcp/03_mcp_client.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Spawn the server as a subprocess. Open an MCP ClientSession over stdio. Print the tools the server offered. Call one. Print the result.

## Try this (a tiny experiment)

Run it twice with two different servers (the example and the SOC server). Notice the client code DOESN'T change — that's the whole point of a standard protocol.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
