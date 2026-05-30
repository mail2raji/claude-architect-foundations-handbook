# Practice Questions — Domain 2a — Tool Use (part of Domain 2, 18%)

Sourced from the consolidated Sets A + B (60 questions total).
Only the **7 questions tagged for this domain** appear here.

> Take these timed: ~2 min per question. Then check the answer key at the bottom.

---

### 15. The `tool_result` block belongs in a turn with role:
- A) `assistant`
- B) `system`
- C) `user`
- D) `tool`

### 19. Which `tool_choice` forces Claude to call a SPECIFIC named tool?
- A) `{"type":"auto"}`
- B) `{"type":"any"}`
- C) `{"type":"tool","name":"X"}`
- D) `{"type":"none"}`

### 23. Which is a built-in Anthropic server-side tool?
- A) `web_search`
- B) `gmail_send`
- C) `okta_lookup`
- D) `s3_upload`

### 27. The `is_error: true` flag on a `tool_result` tells Claude to:
- A) Halt immediately
- B) Treat the result as a failure and try to recover (often retry or pick a different approach)
- C) Echo the error
- D) Switch to Opus

### 36. A `tool_use` block in a response always contains:
- A) `name`, `id`, `input`
- B) `name`, `id`, `output`
- C) `name`, `result`, `error`
- D) `tool_call_id` only

### 37. After an `assistant` turn containing one or more `tool_use` blocks, the next turn must:
- A) Be a fresh `user` text request
- B) Be a `user` turn containing matching `tool_result` blocks (one per `tool_use_id`)
- C) Be a `system` rewrite
- D) Re-send the original prompt

### 43. In a tool definition, the field Claude reads to decide WHEN to call the tool is:
- A) `name`
- B) `description`
- C) `input_schema`
- D) `tool_choice`


---

## Answer key

| # | Ans | Source phase |
|---|---|---|
| 15 | C | Phase 4 |
| 19 | C | Phase 4 |
| 23 | A | Phase 4 |
| 27 | B | Phase 4 |
| 36 | A | Phase 4 |
| 37 | B | Phase 4 |
| 43 | B | Phase 4 |
