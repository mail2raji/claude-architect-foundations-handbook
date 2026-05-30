# Harder Exercises — Domain 4a — Claude API basics (part of Domain 4, 20%)

Subset of the cross-domain 'harder exercises' file, filtered to this domain.
Each exercise expects an architect-level answer, not a tutorial-follower answer.

## (was Phase 2) API Basics (harder)


**2H-1.** Write a wrapper `call_with_jitter_retry(fn, max_retries=3)` that retries on `429` and `5xx` only, with exponential backoff + jitter, and bubbles up other errors.

**2H-2.** Stream a response, but interrupt it cleanly if the stream contains the word "password" (simulating a leakage filter). Return the partial result + a flag.

**2H-3.** Build a function `count_input_tokens_estimate(messages)` using `client.messages.count_tokens` (or your own approximation) and use it to refuse calls that exceed 150K input tokens.

**2H-4.** Produce strict JSON for the schema `{ "categories": ["billing", "tech", "refund"], "confidence": 0..1 }` THREE different ways: (a) prefill `{`, (b) tool-use-as-formatter, (c) plain instruction + post-parse with retry. Measure success rate on 50 inputs.

---
