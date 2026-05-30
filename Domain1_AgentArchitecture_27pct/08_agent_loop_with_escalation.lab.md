# Lab guide — `08_agent_loop_with_escalation.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`08_agent_loop_with_escalation.py`](08_agent_loop_with_escalation.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

Same as the ReAct agent, but if Claude tries the same thing twice and fails, it asks a human for help.

## Why we do this (story time)

Like a kid trying to open a jar. After two tries, instead of breaking the jar, the kid yells 'MOM!'. That 'MOM!' is the escalation — better than a smashed jar.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

The agent runs a loop. If two consecutive tool calls error, it stops and prints an escalation message instead of looping forever.

## Try this (a tiny experiment)

Force the tool to always fail (raise an exception). Watch the escalation fire after 2 retries instead of burning your whole token budget.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
