# Lab guide — `02_mcp_server.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`02_mcp_server.py`](02_mcp_server.py)
> Domain 2 — MCP (part of the 18% Tool/MCP domain).

---

## What this script does

Builds a tiny MCP 'server' — a little program that exposes some tools so OTHER apps (like Claude Desktop) can use them.

## Why we do this (story time)

Like a lemonade stand. You set up the table (the server), and anyone walking by (the clients) can buy lemonade. You don't decide who drinks it — you just keep the stand open.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/mcp/02_mcp_server.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We define an `add` tool and a `greeting` resource using FastMCP, then `mcp.run()` starts a stdio listener. Until a client connects you see nothing — that's normal.

## Try this (a tiny experiment)

Add a second tool that returns the current time. Restart. Now ANY MCP client (Claude Desktop, Claude Code, this repo's bridge) can call it without changing the client.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
