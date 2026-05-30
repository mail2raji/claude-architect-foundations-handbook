# Harder Exercises — Domain 4b — Prompt Engineering & Evaluation (part of Domain 4, 20%)

Subset of the cross-domain 'harder exercises' file, filtered to this domain.
Each exercise expects an architect-level answer, not a tutorial-follower answer.

## (was Phase 3) Prompt Engineering (harder)


**3H-1.** Take a vague prompt ("classify the ticket") and improve it through 5 versions, measuring accuracy on a 100-ticket eval set. Plot the per-version score.

**3H-2.** Build a prompt-injection test set (20 examples) and measure how often each of 4 system-prompt strategies blocks it: (a) plain rules, (b) XML-wrapped user content, (c) "data-not-instructions" rule, (d) all three combined.

**3H-3.** Train an LLM-judge that scores answers 1–5 against a rubric. Add a calibration step: re-score the same answers 3 times and report inter-rater variance. Where is the judge unreliable?

**3H-4.** Demonstrate that few-shot beats CoT for *classification* but loses to CoT for *multi-step math*. Use real datasets.

---
