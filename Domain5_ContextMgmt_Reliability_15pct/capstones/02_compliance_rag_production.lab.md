# Lab guide — `02_compliance_rag_production.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`02_compliance_rag_production.py`](02_compliance_rag_production.py)
> Domain 5 — Context management & RAG (15% of the exam).

---

## What this script does

Production-shape RAG for compliance docs: prompt caching + citations + 'I don't know' guard + audit log.

## Why we do this (story time)

Like a courtroom transcript bot: every claim must point to the page it came from, every query is logged, and if the answer isn't in the file the bot is REQUIRED to say so.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain5_ContextMgmt_Reliability_15pct/capstones/02_compliance_rag_production.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Wraps the hybrid+rerank pipeline with: (a) cache_control on the static system rules, (b) strict `[chunk_id]` citation, (c) refusal phrasing, (d) JSONL audit log per query.

## Try this (a tiny experiment)

Remove the audit log line and ship it — then try to debug a wrong answer 3 days later. You can't. That's why the boring log line is mandatory.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
