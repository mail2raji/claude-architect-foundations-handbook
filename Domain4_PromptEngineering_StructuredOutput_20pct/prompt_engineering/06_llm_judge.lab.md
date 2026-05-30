# Lab guide — `06_llm_judge.py`

**Plain-English explanation. Imagine you're explaining this script to a 5-year-old.**

> Code file: [`06_llm_judge.py`](06_llm_judge.py)
> Domain 4 — Prompt engineering (part of the 20% Prompt/Output domain).

---

## What this script does

Asks a STRONGER Claude to grade a WEAKER Claude's reply on a 1–5 rubric.

## Why we do this (story time)

Like having a school-teacher grade homework done by a student. The teacher is more careful and uses a rubric — even if the student did okay, the teacher catches the small mistakes.

## How to run it

```powershell
# from the repo root (C:\Scripts\Send-escalationEmail\Claude_Learning\)
python Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/06_llm_judge.py
```

Make sure your `ANTHROPIC_API_KEY` is set in `.env` first — see [SETUP.md](../../SETUP.md) if not.

## What you'll see

Sonnet drafts a customer reply. Opus reads the rubric + the reply and outputs a numeric score and a one-line reason. If the score is <4, you re-roll the draft.

## Try this (a tiny experiment)

Score the SAME reply 3 times. Note the variance (it's never zero). That variance is why judges need rubrics — and why you should measure inter-rater reliability before trusting one.

---

*Part of the Claude Certified Architect — Foundations handbook. The full hands-on path is in [LAB_GUIDE.md](../../LAB_GUIDE.md); this file is the kid-friendly companion to the script next to it.*
