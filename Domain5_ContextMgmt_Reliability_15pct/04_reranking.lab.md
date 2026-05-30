# Lab guide — `04_reranking.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`04_reranking.py`](04_reranking.py)
> Domain 5 — Context management & RAG (15% of the exam).

---

## What this script does

Takes the top-25 from search and asks a smarter (slower) model to reorder them by true relevance.

## Why we do this (story time)

Like a talent show: 25 kids audition (cheap), the judges (expensive) only watch the top finalists and pick the winner. Two-stage so you don't watch all 25 carefully.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain5_ContextMgmt_Reliability_15pct/04_reranking.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

We call retrieval (cheap), get top-25, then a cross-encoder reranker scores each (query, candidate) pair and we keep top-5.

## Try this (a tiny experiment)

Skip rerank and feed the top-5 raw retrieval into Claude. Then add rerank and compare answer quality. The rerank step is the highest-leverage upgrade in production RAG.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
