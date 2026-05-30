# Practice Questions Set C (HARD, scenario-based) — Domain 4a — Claude API basics (part of Domain 4, 20%)

Sourced from the consolidated Set C (30 questions total). Each is a real-production scenario; many have plausible distractors.

Only the **9 questions tagged for this domain** appear here.

> Treat these as exam practice: read twice, eliminate clearly wrong answers, only then pick.

---

### 4. You have a static 30K-token system prompt for a chatbot used by 5,000 users/hour. The naive cost is too high. Which is the BEST single change?
- A) Switch all calls to Haiku
- B) Apply `cache_control: ephemeral` to the static prefix
- C) Switch to Batch API
- D) Shorten the system prompt to 5K tokens by removing examples

### 5. A workflow needs to extract 10 fields from a contract and return strict JSON. The contract is 30 pages. Which combination is best?
- A) Sonnet + tool-use-as-formatter for the 10-field schema
- B) Opus + raw JSON in the text
- C) Haiku + prefilling `{`
- D) Two Haiku calls and voting

### 7. A bank wants Claude to read a transaction stream and flag fraud. p99 < 200 ms required. Best architecture?
- A) Sonnet on every transaction
- B) Haiku on every transaction
- C) Classical ML in the hot path; Claude offline for labeling and rule mining
- D) Opus for every transaction with caching

### 11. Which is the MOST common cause of a chatbot bill suddenly doubling overnight?
- A) Anthropic raised prices
- B) Output verbosity grew because someone removed a "be concise" rule or changed model snapshot
- C) Embedding model changed
- D) Cache TTL expired

### 15. You have 1M historical tickets to classify into 12 categories. Latency doesn't matter. Best cost strategy?
- A) Sonnet realtime
- B) Haiku via Batch API
- C) Opus once, cache the answer
- D) Stream Sonnet outputs

### 16. A team's prompt-caching savings are 0% despite a long system prompt. Most likely cause?
- A) The cache TTL expired between calls (>5 min)
- B) Sonnet doesn't support caching
- C) `temperature=0` disables caching
- D) `system` field can't be cached

### 17. Which of these will MOST reliably yield strict, schema-conformant JSON?
- A) "Reply only in JSON" in the system prompt
- B) Prefilling assistant turn with `{`
- C) Tool-use-as-formatter with the schema as the tool's input_schema
- D) Extended thinking

### 20. Which is FALSE about Anthropic prompt caching?
- A) It uses an `ephemeral` cache type with ~5-minute TTL
- B) The first call writes the cache at full input price
- C) Subsequent reads are billed at a fraction of input price
- D) It works across different API keys for the same content

### 24. A vision use case: extract structured data from a scanned receipt. Best approach?
- A) Single Sonnet call with image + tool-use-as-formatter for the schema
- B) OCR locally, then Haiku for parsing
- C) Opus only
- D) Either A or B; pick by cost/quality eval


---

## Answer key with explanations

| # | Ans | Source phase | Why |
|---|---|---|---|
| 4 | **B** | Phase 1 | Caching the static prefix yields ~90% input-token savings without changing behavior. Tier switching may degrade quality; Batch is async. |
| 5 | **A** | Phase 2 | Tool-use-as-formatter gives schema validation for free. Prefilling is fragile across long inputs; voting wastes calls. |
| 7 | **C** | Phase 1 | Honest answer: no LLM hits 200 ms p99 reliably. Use a classical model in the hot path; Claude is the offline labeler. The exam tests if you know LLMs aren't always the answer. |
| 11 | **B** | Phase 1 | The single most common cost incident in production. Output tokens × 5 input cost. Snapshot upgrades often change verbosity defaults. |
| 15 | **B** | Phase 1 | Batch API ~50% off + Haiku tier = cheapest correct mix. Sonnet realtime is 10× more expensive. |
| 16 | **A** | Phase 1 | The cache is ephemeral (~5 min). If traffic is sparse, it expires. Either keep traffic warm or accept lower hit rate. |
| 17 | **C** | Phase 2 | Tool-use-as-formatter is the only approach that gets schema-validated outputs. The model literally must conform. |
| 20 | **D** | Phase 1 | Caches are tied to your prefix + your API account context; they don't share across different API keys. The 5-minute TTL and first-call-writes-cache are correct. |
| 24 | **D** | Phase 2 | The correct exam-style answer is "depends — eval both." OCR-then-LLM is often cheaper and more reliable; direct vision is simpler. Decide with data. |
