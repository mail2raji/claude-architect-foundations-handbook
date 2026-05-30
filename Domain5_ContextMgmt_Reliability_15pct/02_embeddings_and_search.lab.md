# Lab guide — `02_embeddings_and_search.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`02_embeddings_and_search.py`](02_embeddings_and_search.py)
> Domain 5 — Context management & RAG (15% of the exam).

---

## What this script does

Turns text into numbers ('embeddings') so the computer can find chunks SIMILAR in meaning, not just chunks with the same words.

## Why we do this (story time)

Like sorting socks by colour AND by fuzziness instead of by alphabet. 'I love dogs' and 'puppies are great' have NO words in common, but the meaning is close — embeddings catch that.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain5_ContextMgmt_Reliability_15pct/02_embeddings_and_search.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

We embed a small corpus + the query using Voyage AI, then take cosine similarity. The top-3 chunks are printed with their scores.

## Try this (a tiny experiment)

Search for 'puppy' against a corpus that only mentions 'dog' — embeddings still find it. Word matching ('grep') wouldn't.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
