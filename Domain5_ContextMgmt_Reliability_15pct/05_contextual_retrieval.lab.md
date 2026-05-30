# Lab guide — `05_contextual_retrieval.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`05_contextual_retrieval.py`](05_contextual_retrieval.py)
> Domain 5 — Context management & RAG (15% of the exam).

---

## What this script does

Before embedding each chunk, asks Claude to write a 1-paragraph 'context' that explains where the chunk came from. Boosts retrieval ~50%.

## Why we do this (story time)

Imagine each puzzle piece had a tiny sticker saying 'I'm a corner piece from the sky bit'. Way easier to assemble than blank pieces.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain5_ContextMgmt_Reliability_15pct/05_contextual_retrieval.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

For every chunk we send Claude the WHOLE doc + the chunk and ask for a context paragraph. We prepend it to the chunk text BEFORE embedding. Prompt caching keeps cost flat.

## Try this (a tiny experiment)

Disable prompt caching and time the run. It's ~10× slower / more expensive. Caching is the trick that makes contextual retrieval affordable.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
