# Lab guide — `03_hybrid_bm25.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`03_hybrid_bm25.py`](03_hybrid_bm25.py)
> Domain 5 — Context management & RAG (15% of the exam).

---

## What this script does

Combines word-matching (BM25) with meaning-matching (vectors) — the best of both worlds.

## Why we do this (story time)

Like searching the library with BOTH the title catalogue (exact words) AND the subject catalogue (themes). You catch books neither catalogue alone would find.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain5_ContextMgmt_Reliability_15pct/03_hybrid_bm25.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

We run BM25 and vectors separately on the same query. Then we fuse the two ranked lists with reciprocal rank fusion (RRF). The fused top-3 is usually better than either alone.

## Try this (a tiny experiment)

Try a query like 'Section 4.2 refund'. BM25 wins (exact tokens). Then try 'how do I get my money back'. Vectors win. Hybrid wins both.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
