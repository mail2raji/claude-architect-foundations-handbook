# Lab guide — `mini_project_kb_qa.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`mini_project_kb_qa.py`](mini_project_kb_qa.py)
> Domain 5 — Context management & RAG (15% of the exam).

---

## What this script does

End-to-end Q&A bot over an internal IT knowledge base — chunk → embed → hybrid retrieve → rerank → answer with citations.

## Why we do this (story time)

It's the whole library: someone cuts the books into pages (chunk), the librarian indexes them (embed + bm25), a senior librarian picks the best pages (rerank), and a friendly assistant reads them aloud with page numbers (cite).

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain5_ContextMgmt_Reliability_15pct/mini_project_kb_qa.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../SETUP.md) if not.

## What you'll see

Loads a tiny mock corpus. You type a question. The pipeline retrieves the top chunks and feeds them to Claude with a 'cite [chunk_id]' rule. Answer includes citations.

## Try this (a tiny experiment)

Ask a question whose answer is NOT in the corpus. A well-guarded bot says 'I don't know'. Check yours does — that's the single biggest hallucination fix.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
