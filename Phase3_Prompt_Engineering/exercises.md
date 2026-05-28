# Phase 3 — Exercises

1. Add a 5th prompt to `05_eval_framework.py` that uses **few-shot** (3 examples) in addition to XML+rules+CoT. Does it beat v4?
2. Extend the LLM-judge to also output a 1-sentence rationale (`<rationale>`). Save (score, rationale) pairs to a CSV.
3. Build a "self-critique" loop: ask Claude to draft a reply, then in a 2nd turn ask itself "what could be wrong?", then revise. Compare with a single-shot reply via LLM-judge.
4. Pick one of the prompts from your existing PowerShell scripts (`Send-EscalationEmail.ps1`) and rewrite the LLM-facing portion (if any) using XML tags.

## Mini quiz answers (from README)

1. **Multi-shot / few-shot examples** — almost always the largest lift.
2. **Top.** Question/instruction goes at the bottom — Claude attends most strongly to what's near the end.
3. Prefilling = putting text in the **assistant** role at the end of `messages` so the model continues from your seed (`{`, `Step 1.`, ` ```powershell\n`, …).
4. **Ground-truth (deterministic), LLM-as-judge, code/heuristic.**
5. Removing randomness so your evals measure *prompt* quality, not sampling luck.
