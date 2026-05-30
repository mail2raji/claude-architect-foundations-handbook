# Lab guide — `01_soc_triage_pipeline.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`01_soc_triage_pipeline.py`](01_soc_triage_pipeline.py)
> Domain 1 — Agent Architecture (27% of the exam).

---

## What this script does

Reads security alerts and decides which need a human, which can be auto-closed, and which need more digging.

## Why we do this (story time)

Like a hospital ER triage nurse: 'You go home, you sit down, YOU come with me right now'. The pipeline sorts a flood of alerts into three buckets so analysts only see the real fires.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain1_AgentArchitecture_27pct/capstones/01_soc_triage_pipeline.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Each alert is tagged with severity + recommended action by Claude. Auto-close happens for low confidence noise. Hard cases get enriched and queued for a human.

## Try this (a tiny experiment)

Change the auto-close threshold (e.g. only close if confidence > 0.95). Watch the auto-closed count drop and human queue grow. That trade-off is the heart of production triage.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
