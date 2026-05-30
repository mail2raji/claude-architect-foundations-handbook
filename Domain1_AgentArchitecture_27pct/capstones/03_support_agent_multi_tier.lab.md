# Lab guide — `03_support_agent_multi_tier.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`03_support_agent_multi_tier.py`](03_support_agent_multi_tier.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

A customer-support agent that uses cheap Claude first, and only escalates to the smart (expensive) Claude when stuck.

## Why we do this (story time)

Like a phone tree: first you talk to a robot, then a junior agent, then a supervisor. Most calls stop at the robot. That's why your phone bill is small.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/capstones/03_support_agent_multi_tier.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Tier 1 = Haiku (fast/cheap). Tier 2 = Sonnet (smarter). Tier 3 = human escalation message. Each question is tried at the cheapest tier first.

## Try this (a tiny experiment)

Change a Haiku confidence threshold and re-run a hard question. Watch it bubble up to Sonnet. This pattern is THE single biggest cost-saver in production chatbots.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
