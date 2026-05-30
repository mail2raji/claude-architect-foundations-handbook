# Lab guide — `mini_project_research_agent.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`mini_project_research_agent.py`](mini_project_research_agent.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

Glues router + orchestrator + parallel workers + evaluator all together to research a question end-to-end.

## Why we do this (story time)

It's the whole kitchen: the host (router) seats you, the head chef (orchestrator) plans the meal, line cooks (workers) cook each dish, and the food critic (evaluator) tastes it before it goes out.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/mini_project_research_agent.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

You ask a research question. The router decides it IS research (not small talk). The orchestrator writes sub-questions. Workers each answer one in parallel. The evaluator checks the brief cites ≥ 2 sources and re-rolls if not.

## Try this (a tiny experiment)

Ask it small talk ('hello!'). The router should short-circuit the whole pipeline. That single check saves you the cost of running the orchestrator + workers + evaluator on a 'hi'.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
