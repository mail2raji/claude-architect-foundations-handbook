# Practice Questions — Domain 4b — Prompt Engineering & Evaluation (part of Domain 4, 20%)

Sourced from the consolidated Sets A + B (60 questions total).
Only the **6 questions tagged for this domain** appear here.

> Take these timed: ~2 min per question. Then check the answer key at the bottom.

---

### 4. Which prompting technique typically gives the LARGEST accuracy lift on classification?
- A) Increasing `max_tokens`
- B) Switching to Opus
- C) Adding 3–5 few-shot examples
- D) Lowering `temperature`

### 5. For long documents in a prompt, put them:
- A) At the bottom, near the question
- B) At the top, with the question at the bottom
- C) Inside the system prompt
- D) Split across multiple user turns

### 22. Extended thinking is enabled in the API via:
- A) `temperature=0.0`
- B) `thinking={"type":"enabled","budget_tokens":...}`
- C) `system="think step by step"`
- D) Setting `max_tokens` higher

### 40. Which is FALSE about XML tags in Claude prompts?
- A) They must be syntactically valid XML
- B) They help Claude attend to sections
- C) They are great for delimiting `<context>`, `<task>`, `<examples>`
- D) Claude was trained to respect them

### 42. The most appropriate model tier for an LLM-judge over open-ended outputs is usually:
- A) Haiku
- B) Sonnet
- C) Opus
- D) Mix of all three

### 59. Strong few-shot examples should be placed:
- A) Inside the system prompt only
- B) Inside `<examples>` XML tags before the new question
- C) After the answer
- D) Only as `assistant` turns


---

## Answer key

| # | Ans | Source phase |
|---|---|---|
| 4 | C | Phase 3 |
| 5 | B | Phase 3 |
| 22 | B | Phase 3 |
| 40 | A | Phase 3 |
| 42 | C | Phase 3 |
| 59 | B | Phase 3 |
