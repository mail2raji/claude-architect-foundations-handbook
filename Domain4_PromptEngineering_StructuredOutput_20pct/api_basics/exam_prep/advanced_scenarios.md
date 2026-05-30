# Advanced Architectural Scenarios — Domain 4a — Claude API basics (part of Domain 4, 20%)

Sourced from the consolidated 25 cross-domain scenarios.
Only the **6 scenarios tagged for this domain** appear here.

Sketch an architecture answer first, then compare to the solution sketch at the bottom.

---

## Exercises

**E9.** A consumer app classifies images of food into 80 dish categories. Vision support is required. Architect.

**E10.** A fraud team wants a real-time scorer for new transactions. p99 < 300 ms. Architect.

**E16.** Cost review: a chatbot's bill jumped 4× last week. Where do you look first?

**E17.** Quality regression: after upgrading Sonnet's snapshot, summary length is up 30% and users complain. Diagnose and fix.

**E20.** A 200K-token system prompt is reused for every user. The bill is enormous. Fix.

**E21.** You want strict, schema-validated JSON output from a classifier with 7 enum values. Three approaches — rank them by reliability.


---
## Solution sketches

**A9.** Claude vision call (Sonnet) with a structured-output tool returning `{"dish": "...", "confidence": 0..1}`. Top-1 of 80 enum values. Fallback to "unsure" below confidence threshold. Likely you'd actually use a CV model for cost; Claude is best as a fallback "unsure" reviewer.

**A10.** Don't use an LLM in the hot path for 300 ms p99. Use a classical model. Use Claude offline to label data + tune thresholds. (Trick exam answer: "don't use an LLM" is sometimes the right pattern.)

**A16.** Check (a) output token length blow-up — did you remove a "be concise" instruction? (b) is the static prefix still being cached? (c) is something looping in an agent without `max_steps`? (d) did traffic mix shift toward Opus?

**A17.** New snapshot is verbose by default. Add "answer in <=60 words" and adjust `max_tokens`. Or pin a previous snapshot until you migrate. Run the eval harness to confirm.

**A20.** Set `cache_control: ephemeral` on the static prefix. Restructure prompt: static at top (cached), variable at bottom. Renew cache via traffic. ~90% savings on input tokens after the first call.

**A21.** (Most reliable → least) **Tool-use-as-formatter with enum constraint** > **Prefill `{"label": "`** > free-text "respond with JSON". Tool-as-formatter is the only one that gets schema validation for free.
