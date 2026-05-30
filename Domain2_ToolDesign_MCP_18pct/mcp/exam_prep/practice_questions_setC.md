# Practice Questions Set C (HARD, scenario-based) — Domain 2b — Model Context Protocol (part of Domain 2, 18%)

Sourced from the consolidated Set C (30 questions total). Each is a real-production scenario; many have plausible distractors.

Only the **3 questions tagged for this domain** appear here.

> Treat these as exam practice: read twice, eliminate clearly wrong answers, only then pick.

---

### 13. You're designing an MCP server that exposes 30 internal APIs. You want Claude to decide *when* to call each. They should appear as:
- A) Resources
- B) Tools
- C) Prompts
- D) Capabilities

### 14. The same MCP server wants to surface "today's incidents" so the user can attach them to their conversation. These should be:
- A) Resources, identified by URI
- B) Tools
- C) Prompts
- D) Capabilities

### 25. An MCP "prompt" primitive is BEST described as:
- A) An LLM call the server makes
- B) A pre-templated, user-invoked workflow (e.g., a slash command)
- C) A vector embedding
- D) A system prompt fragment


---

## Answer key with explanations

| # | Ans | Source phase | Why |
|---|---|---|---|
| 13 | **B** | Phase 6 | Tools = MODEL-invoked. APIs the LLM decides to call → tools. |
| 14 | **A** | Phase 6 | Resources = APP/USER-attached, identified by URI. Today's incidents are pickable context items. |
| 25 | **B** | Phase 6 | Prompt = user-invoked workflow template (e.g., slash-command). Not an LLM call, not embeddings. |
