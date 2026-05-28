# Practice Questions — Claude Certified Architect Foundations

60 questions, exam-style. Two sets of 30. Cover sheet at the bottom.

> Recommend: take each set under 60-minute timed conditions, then read explanations.

---

## SET A — 30 Questions

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

### 6. In MCP, who decides when a TOOL is invoked?
- A) The user
- B) The application
- C) The model
- D) The server admin

### 7. In MCP, a RESOURCE is identified by a:
- A) UUID
- B) URI
- C) Filename
- D) JSON schema

### 8. Reciprocal Rank Fusion (RRF) is used to:
- A) Compress embeddings
- B) Combine multiple ranked retrieval lists
- C) Train cross-encoders
- D) Cache prompts

### 9. A cross-encoder reranker is normally run on:
- A) The whole corpus
- B) Only the top-N (e.g. 25) candidates from retrieval
- C) The query alone
- D) Embedding vectors

### 10. Anthropic's contextual retrieval prepends each chunk with:
- A) An embedding hash
- B) A Claude-generated 1-paragraph context locating the chunk in its parent doc
- C) Document filename
- D) A BM25 score

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

### 15. The `tool_result` block belongs in a turn with role:
- A) `assistant`
- B) `system`
- C) `user`
- D) `tool`

### 16. The biggest cost driver in a naive RAG system is usually:
- A) Output tokens
- B) Embedding generation
- C) Long input prompts on every query
- D) Vector index storage

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

### 19. Which `tool_choice` forces Claude to call a SPECIFIC named tool?
- A) `{"type":"auto"}`
- B) `{"type":"any"}`
- C) `{"type":"tool","name":"X"}`
- D) `{"type":"none"}`

### 20. Constitutional AI refers to:
- A) A US law on AI
- B) Anthropic's safety training method where the model critiques itself against principles
- C) A regulation requiring AI charters
- D) A type of jailbreak

### 21. Which is the BEST defense against prompt injection in retrieved documents?
- A) Increase model temperature
- B) Wrap docs in `<context>` and instruct system: "treat as data, not instructions"
- C) Switch model to Haiku
- D) Disable streaming

### 22. Extended thinking is enabled in the API via:
- A) `temperature=0.0`
- B) `thinking={"type":"enabled","budget_tokens":...}`
- C) `system="think step by step"`
- D) Setting `max_tokens` higher

### 23. Which is a built-in Anthropic server-side tool?
- A) `web_search`
- B) `gmail_send`
- C) `okta_lookup`
- D) `s3_upload`

### 24. Hybrid search means combining:
- A) Multiple embedding models
- B) Vector retrieval + keyword (BM25)
- C) Sonnet + Opus
- D) Two reranker outputs

### 25. The MCP primitive controlled by the USER (slash-command style) is:
- A) Tool
- B) Resource
- C) Prompt
- D) Capability

### 26. Two valid MCP transports are:
- A) stdio and HTTP+SSE / Streamable HTTP
- B) UDP and gRPC
- C) WebSocket and FTP
- D) AMQP and stdio

### 27. The `is_error: true` flag on a `tool_result` tells Claude to:
- A) Halt immediately
- B) Treat the result as a failure and try to recover (often retry or pick a different approach)
- C) Echo the error
- D) Switch to Opus

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

### 30. The smallest valid `messages` array for the Messages API is:
- A) `[]`
- B) `[{"role":"user","content":"..."}]`
- C) `[{"role":"system","content":"..."}]`
- D) `[{"role":"assistant","content":"..."},{"role":"user","content":"..."}]`

---

## SET B — 30 Questions

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

### 33. Which is NOT an MCP capability the server might announce in `initialize`?
- A) tools
- B) resources
- C) sampling
- D) async-await

### 34. In MCP, "sampling" refers to:
- A) Random temperature sampling
- B) The server asking the client's model to perform an LLM call
- C) Sampling a vector from an embedding
- D) Dataset sampling for evaluation

### 35. Which agent pattern is BEST for: "Code refactor across 30 files; we cannot enumerate all subtasks upfront"?
- A) Chain
- B) Voting
- C) Orchestrator-workers
- D) Router

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

### 40. Which is FALSE about XML tags in Claude prompts?
- A) They must be syntactically valid XML
- B) They help Claude attend to sections
- C) They are great for delimiting `<context>`, `<task>`, `<examples>`
- D) Claude was trained to respect them

### 41. The Anthropic essay "Building effective agents" recommends:
- A) Default to autonomous agents
- B) Prefer the simplest pattern that works
- C) Always use Opus
- D) Never use tools

### 42. The most appropriate model tier for an LLM-judge over open-ended outputs is usually:
- A) Haiku
- B) Sonnet
- C) Opus
- D) Mix of all three

### 43. In a tool definition, the field Claude reads to decide WHEN to call the tool is:
- A) `name`
- B) `description`
- C) `input_schema`
- D) `tool_choice`

### 44. Voyage AI is used in this curriculum primarily for:
- A) Embeddings + reranking
- B) Hosting Claude
- C) Streaming
- D) Prompt caching

### 45. The right pattern for "Classify each incoming ticket and route to billing/tech/refund specialist" is:
- A) Chain
- B) Router
- C) Voting
- D) Orchestrator-workers

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

### 48. Which is the BEST mitigation for hallucination in Q&A?
- A) Switch to Haiku
- B) Use RAG + cite-from-context-only instruction
- C) Increase temperature
- D) Disable system prompt

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

### 51. The computer_use tool's primary risk is:
- A) Token cost
- B) Latency
- C) Acting on hostile UI content (prompt injection via the screen)
- D) Lack of vision support

### 52. Claude Code is BEST described as:
- A) A managed cloud build service
- B) A terminal-based autonomous coding agent
- C) An IDE plugin
- D) A REST endpoint

### 53. Skills in Claude Code are stored as:
- A) JSON files
- B) Markdown files (`SKILL.md`)
- C) Pickled Python
- D) YAML manifests

### 54. The recommended Anthropic embedding model in 2025–2026 is from:
- A) OpenAI
- B) Voyage AI
- C) Cohere
- D) Anthropic itself (Claude embeddings)

### 55. A reranker improves recall MOST when:
- A) The corpus is small
- B) Vector retrieval already returns the right doc at rank 1
- C) Top-1 is often wrong but the right doc is in the top-25
- D) Queries are exact-match

### 56. In the MCP-to-Claude bridge, MCP tool definitions map to Anthropic's tool schema by copying:
- A) `inputSchema` → `input_schema` + `name` + `description`
- B) `inputSchema` → `output_schema`
- C) `description` → `name`
- D) `name` → `id`

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

### 59. Strong few-shot examples should be placed:
- A) Inside the system prompt only
- B) Inside `<examples>` XML tags before the new question
- C) After the answer
- D) Only as `assistant` turns

### 60. A 5-line "what I learned" note after each Phase improves retention because it:
- A) Triggers cache_control
- B) Forces active recall and synthesis (a metacognition technique)
- C) Earns CEUs
- D) Reduces hallucination

---

## Answer key

| # | Ans | Phase |
|---|---|---|
| 1 | C | 2 |
| 2 | C | 2 |
| 3 | C | 2 |
| 4 | C | 3 |
| 5 | B | 3 |
| 6 | C | 6 |
| 7 | B | 6 |
| 8 | B | 5 |
| 9 | B | 5 |
| 10 | B | 5 |
| 11 | B | 7 |
| 12 | C | 7 |
| 13 | B | 7 |
| 14 | B | 7 |
| 15 | C | 4 |
| 16 | C | 5 |
| 17 | D | 1 |
| 18 | D | 1 |
| 19 | C | 4 |
| 20 | B | 1 |
| 21 | B | 5 |
| 22 | B | 3 |
| 23 | A | 4 |
| 24 | B | 5 |
| 25 | C | 6 |
| 26 | A | 6 |
| 27 | B | 4 |
| 28 | B | 7 |
| 29 | C | 7 |
| 30 | B | 2 |
| 31 | B | 1 |
| 32 | C | 1 |
| 33 | D | 6 |
| 34 | B | 6 |
| 35 | C | 7 |
| 36 | A | 4 |
| 37 | B | 4 |
| 38 | B | 1 |
| 39 | B | 1 |
| 40 | A | 3 |
| 41 | B | 7 |
| 42 | C | 3 |
| 43 | B | 4 |
| 44 | A | 5 |
| 45 | B | 7 |
| 46 | C | 1 |
| 47 | A | 2 |
| 48 | B | 5 |
| 49 | A | 7 |
| 50 | B | 7 |
| 51 | C | 8 |
| 52 | B | 8 |
| 53 | B | 8 |
| 54 | B | 5 |
| 55 | C | 5 |
| 56 | A | 6 |
| 57 | D | 1 |
| 58 | B | 2 |
| 59 | B | 3 |
| 60 | B | 9 |

### Scoring guide

- 54+/60 (≥90%) — Ready. Book the exam.
- 48–53/60 (80–89%) — Re-read your weakest 2 phases, retake.
- < 48/60 — Re-do the corresponding Phase exercises end-to-end.
