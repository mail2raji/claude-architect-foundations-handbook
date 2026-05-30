# Lab guide — `06_vision.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`06_vision.py`](06_vision.py)
> Domain 4 — Claude API basics (part of the 20% Prompt/Output domain).

---

## What this script does

Sends an IMAGE to Claude (not just text) and asks it to describe what's in the picture.

## Why we do this (story time)

Like showing grandma a photo and asking 'what's happening here?'. The eyes do the work — same idea, just Claude's eyes.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/06_vision.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

We attach an image content block (URL or base64). Claude returns text describing what it saw. Works on PNG/JPG/GIF/WEBP.

## Try this (a tiny experiment)

Use a picture of a network diagram and ask 'spot security weaknesses'. Vision turns Claude into an architecture reviewer for diagrams you'd normally only show humans.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
