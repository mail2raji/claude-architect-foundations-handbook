# Lab guide — `04_it_triage_agent.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`04_it_triage_agent.py`](04_it_triage_agent.py)
> Domain 2 — Tool design (part of the 18% Tool/MCP domain).

---

## What this script does

An IT helpdesk agent that picks the right tool — search KB, check user, create ticket — from a few options.

## Why we do this (story time)

Like a school office that has 'lost-and-found', 'sick room', 'principal'. The receptionist picks one based on what you say. The receptionist isn't smart — but knowing WHICH door to send you through is enough.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain2_ToolDesign_MCP_18pct/tool_use/04_it_triage_agent.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

User says 'I can't log in'. Agent picks search_kb('login'), reads results, picks check_user_status('alice'), then picks create_ticket(...) if still broken. Each pick is shown so you can grade the route.

## Try this (a tiny experiment)

Add a deliberately ambiguous tool (e.g. `search_anywhere`). Watch Claude get confused. Then fix it by improving the tool description. That ONE skill is half of Domain 2.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
