# Lab guide — `07_react_agent.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`07_react_agent.py`](07_react_agent.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

Claude is given tools and decides — by itself — which tool to use, when, and when to stop.

## Why we do this (story time)

Think of a treasure hunt: you read a clue, decide whether to look in the kitchen or the garden, look, see what you found, then read the next clue. That loop of 'think → act → see → think again' is ReAct.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/07_react_agent.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

Claude is given a weather tool and a calculator. You ask 'what's the temperature in Sydney times 2?'. It calls the weather tool, gets 22, then calls the calculator, gets 44, then answers.

## Try this (a tiny experiment)

Comment out the calculator tool but keep the question. Claude will try to do the math in its head — sometimes wrong. That shows why tools matter for things models are bad at.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
