# Lab guide — `01_chunking.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`01_chunking.py`](01_chunking.py)
> Domain 5 — Context management & RAG (15% of the exam).

---

## What this script does

Cuts a long document into bite-size chunks so search can find the right paragraph instead of returning a whole book.

## Why we do this (story time)

Like cutting pizza into slices: easier to grab the slice you want. A whole pizza is too big to share.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain5_ContextMgmt_Reliability_15pct/01_chunking.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

We split a text by paragraph, then enforce a max-character chunk size with overlap so important context isn't sliced in half. The output is a list of chunk strings.

## Try this (a tiny experiment)

Try chunk_size=50 vs chunk_size=2000 on the same doc. Tiny chunks miss context; huge chunks dilute relevance. Pick the size that fits your retrieval depth.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
