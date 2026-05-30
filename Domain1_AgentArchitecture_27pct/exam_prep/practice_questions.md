# Practice Questions — Domain 1 — Agent Architecture & Orchestration (27%)

Sourced from the consolidated Sets A + B (60 questions total).
Only the **12 questions tagged for this domain** appear here.

> Take these timed: ~2 min per question. Then check the answer key at the bottom.

---

### 11. Which pattern best fits: "Same input, ask Claude 5 times, take majority vote"?
- A) Routing
- B) Parallelization (voting)
- C) Orchestrator-workers
- D) Evaluator-optimizer

### 12. Which pattern best fits: "A planner LLM splits the work, workers run in parallel, planner synthesizes"?
- A) Routing
- B) Chain
- C) Orchestrator-workers
- D) Parallelization (sectioning)

### 13. Anthropic recommends preferring _____ over _____ when both fit.
- A) Agents, workflows
- B) Workflows, agents
- C) Opus, Sonnet
- D) Streaming, non-streaming

### 14. A REQUIRED safety knob on any autonomous agent is:
- A) `temperature=1`
- B) A `max_steps` cap
- C) Streaming enabled
- D) `cache_control`

### 28. The router workflow most directly saves cost by:
- A) Avoiding tool calls
- B) Routing easy questions to Haiku and hard ones to Opus
- C) Caching prompts
- D) Limiting streaming

### 29. The right pattern for *strict-quality* legal copy that must satisfy a rubric is:
- A) Chain
- B) Routing
- C) Evaluator-optimizer
- D) Voting

### 35. Which agent pattern is BEST for: "Code refactor across 30 files; we cannot enumerate all subtasks upfront"?
- A) Chain
- B) Voting
- C) Orchestrator-workers
- D) Router

### 41. The Anthropic essay "Building effective agents" recommends:
- A) Default to autonomous agents
- B) Prefer the simplest pattern that works
- C) Always use Opus
- D) Never use tools

### 45. The right pattern for "Classify each incoming ticket and route to billing/tech/refund specialist" is:
- A) Chain
- B) Router
- C) Voting
- D) Orchestrator-workers

### 49. The right pattern for "Outline → Draft → Polish, in fixed order" is:
- A) Chain
- B) Voting
- C) Router
- D) Evaluator-optimizer

### 50. The right pattern for "Same job done by 5 specialists in parallel, then merge" is:
- A) Chain
- B) Sectioning (parallelization)
- C) Router
- D) Evaluator-optimizer

### 60. A 5-line "what I learned" note after each Phase improves retention because it:
- A) Triggers cache_control
- B) Forces active recall and synthesis (a metacognition technique)
- C) Earns CEUs
- D) Reduces hallucination


---

## Answer key

| # | Ans | Source phase |
|---|---|---|
| 11 | B | Phase 7 |
| 12 | C | Phase 7 |
| 13 | B | Phase 7 |
| 14 | B | Phase 7 |
| 28 | B | Phase 7 |
| 29 | C | Phase 7 |
| 35 | C | Phase 7 |
| 41 | B | Phase 7 |
| 45 | B | Phase 7 |
| 49 | A | Phase 7 |
| 50 | B | Phase 7 |
| 60 | B | Phase 9 |
