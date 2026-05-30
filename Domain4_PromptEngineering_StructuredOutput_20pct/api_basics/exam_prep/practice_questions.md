# Practice Questions — Domain 4a — Claude API basics (part of Domain 4, 20%)

Sourced from the consolidated Sets A + B (60 questions total).
Only the **15 questions tagged for this domain** appear here.

> Take these timed: ~2 min per question. Then check the answer key at the bottom.

---

### 1. Which content role can appear at most once per request?
- A) `user`
- B) `assistant`
- C) `system`
- D) `tool`

### 2. Which `stop_reason` indicates Claude wants to call a tool?
- A) `end_turn`
- B) `max_tokens`
- C) `tool_use`
- D) `pause_turn`

### 3. The most RELIABLE technique to guarantee strict JSON output from Claude is:
- A) Asking nicely in the system prompt
- B) Prefilling the assistant turn with `{`
- C) Tool-use-as-formatter with `tool_choice={"type":"tool","name":...}`
- D) Setting `temperature=0`

### 17. Which is NOT a Claude tier?
- A) Haiku
- B) Sonnet
- C) Opus
- D) Allegro

### 18. The current production context window for Claude is up to:
- A) 4K tokens
- B) 32K tokens
- C) 128K tokens
- D) 200K tokens

### 20. Constitutional AI refers to:
- A) A US law on AI
- B) Anthropic's safety training method where the model critiques itself against principles
- C) A regulation requiring AI charters
- D) A type of jailbreak

### 30. The smallest valid `messages` array for the Messages API is:
- A) `[]`
- B) `[{"role":"user","content":"..."}]`
- C) `[{"role":"system","content":"..."}]`
- D) `[{"role":"assistant","content":"..."},{"role":"user","content":"..."}]`

### 31. Which is BEST suited to Haiku?
- A) Multi-step math proof
- B) High-volume ticket classification
- C) Drafting a 10-page strategy memo
- D) Writing a research brief synthesizing 30 docs

### 32. Output token cost per million is usually:
- A) Cheaper than input
- B) The same as input
- C) More expensive than input
- D) Free for Sonnet

### 38. Prompt caching's TTL is approximately:
- A) 30 seconds
- B) 5 minutes (ephemeral)
- C) 1 hour
- D) 24 hours

### 39. The PRIMARY benefit of prompt caching is:
- A) Faster outputs
- B) Reduced INPUT token billing on repeated prefixes (~90%)
- C) Streaming reliability
- D) Bypassing rate limits

### 46. Which sentence describes the difference between Claude.ai and the API best?
- A) They're identical
- B) Claude.ai is a free version of the API
- C) Claude.ai is a consumer chat product; the API is the developer surface
- D) The API is older and being deprecated

### 47. The Messages API REQUIRES that:
- A) The last message be `user`
- B) The first message be `system`
- C) `assistant` is optional
- D) Conversation begin with `tool_result`

### 57. Which is NOT a recommended way to reduce Claude cost?
- A) Prompt caching for reused prefixes
- B) Batch API for non-realtime jobs
- C) Routing easy queries to Haiku
- D) Always switch to Opus for higher quality

### 58. The `pause_turn` stop reason is reserved for:
- A) Streaming pauses
- B) Long-running flows that must resume later
- C) Errors
- D) Tool calls


---

## Answer key

| # | Ans | Source phase |
|---|---|---|
| 1 | C | Phase 2 |
| 2 | C | Phase 2 |
| 3 | C | Phase 2 |
| 17 | D | Phase 1 |
| 18 | D | Phase 1 |
| 20 | B | Phase 1 |
| 30 | B | Phase 2 |
| 31 | B | Phase 1 |
| 32 | C | Phase 1 |
| 38 | B | Phase 1 |
| 39 | B | Phase 1 |
| 46 | C | Phase 1 |
| 47 | A | Phase 2 |
| 57 | D | Phase 1 |
| 58 | B | Phase 2 |
