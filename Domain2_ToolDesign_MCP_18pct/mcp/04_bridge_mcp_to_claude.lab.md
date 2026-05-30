# Lab guide — `04_bridge_mcp_to_claude.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`04_bridge_mcp_to_claude.py`](04_bridge_mcp_to_claude.py)
> Domain 2 — MCP (part of the 18% Tool/MCP domain).

---

## What this script does

Hooks an MCP server up to Claude as if its tools were Claude's own tools — the bridge Claude Desktop uses.

## Why we do this (story time)

Like a translator at the UN: MCP server speaks one language, Claude speaks another, the bridge translates back and forth so they can have a conversation.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/mcp/04_bridge_mcp_to_claude.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We list the MCP server's tools, convert each to Anthropic tool-schema shape, then run a normal agent loop. When Claude says 'call X', the bridge dispatches X through MCP.

## Try this (a tiny experiment)

Add a new tool to the server (no other changes). The bridge picks it up automatically. That ZERO-glue extension is why MCP exists.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
