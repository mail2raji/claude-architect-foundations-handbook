# Glossary — Claude Certified Architect Foundations

A term is *exam-fair-game* if it appears in either the API docs, the Skilljar courses, or Anthropic's "Building effective agents" essay.

## A
- **Agent** — A loop where the model decides the next tool call based on observations until done. (Phase 7)
- **Allow-list (tools)** — Restricting which tools an agent may call at a given step. Safety knob. (Phase 7)
- **API key** — Secret beginning `sk-ant-`. Authenticates calls to api.anthropic.com. (Phase 0)

## B
- **Bash tool** — Built-in Anthropic tool that runs shell commands in a sandbox. Used by Claude Code. (Phase 4, 8)
- **Batch API** — Async bulk endpoint at ~50% discount. (Phase 1)
- **BM25** — Classic keyword retrieval algorithm. Use alongside vector search for hybrid retrieval. (Phase 5)

## C
- **Cache control / Prompt caching** — Mark content blocks with `cache_control: {type: 'ephemeral'}` to cache the prefix for 5 min; subsequent calls reuse it at ~10% cost. (Phases 1, 5)
- **Chain of thought (CoT)** — Asking the model to think step-by-step in `<thinking>` tags before answering. (Phase 3)
- **Citation** — Asking the model to point to source `[id]` it used. Good RAG hygiene. (Phase 5)
- **Claude Code** — Anthropic's CLI coding agent. (Phase 8)
- **Computer Use** — Server-side tool for mouse/keyboard/screen control of a sandbox VM. (Phase 8)
- **Constitutional AI** — Anthropic's safety training technique (model critiques and revises itself against principles). (Phase 1)
- **Context window** — Maximum total tokens (input + output) per call. Up to 200K for current Claude. (Phase 1)
- **Contextual retrieval** — Anthropic's recipe: prefix each chunk with a Claude-generated paragraph of context before indexing. (Phase 5)
- **Cross-encoder** — A model that takes (query, doc) together and scores relevance. Used in rerankers. (Phase 5)

## E
- **Embedding** — Vector representation of text. Same model for query and doc. (Phase 5)
- **Ephemeral cache** — 5-minute prompt cache TTL. (Phase 1)
- **Evaluator-optimizer** — Generator-and-critic loop until rubric passes. (Phase 7)
- **Extended thinking** — Reasoning mode where the API returns a separate `thinking` content block; enabled with `thinking={"type":"enabled","budget_tokens":...}`. (Phase 3)

## F
- **Few-shot prompting** — Providing 2–5 examples in the prompt. Biggest accuracy lever. (Phase 3)
- **Function calling** — Synonym for tool use. (Phase 4)

## G
- **GDPR / SOX / HIPAA** — Compliance frameworks; the model needs domain context to classify by these. (Phase 3)
- **Gate** — A conditional check between workflow steps. (Phase 7)

## H
- **Haiku** — Smallest/fastest/cheapest Claude tier. (Phase 1)
- **Hallucination** — Confidently wrong output. Mitigations: RAG, tools, evals. (Phase 1, 5)
- **Hybrid search** — Combine vector + BM25 (often via RRF). (Phase 5)

## I
- **`is_error`** — Field on a `tool_result` block; signals tool failed so Claude retries. (Phase 4)
- **`initialize`** — MCP handshake step exchanging capabilities. (Phase 6)

## J
- **Jailbreak** — Adversarial prompt designed to bypass safety. (Phase 1)
- **JSON Schema (`input_schema`)** — Structure for tool inputs (also for MCP). (Phases 2, 4, 6)

## K
- **KQL** — Kusto Query Language (used in the SOC mini-project as a tool input). (Phase 6)

## L
- **LLM-as-judge** — Use Claude to grade Claude's open-ended output against a rubric. (Phase 3)

## M
- **Max tokens** — Cap on OUTPUT tokens per call. Must be set. (Phase 2)
- **Max steps** — Cap on agent loop iterations. Required safety knob. (Phase 7)
- **MCP (Model Context Protocol)** — Standardized client/server protocol for tools/resources/prompts. (Phase 6)
- **Messages API** — Primary chat endpoint: `client.messages.create(...)`. (Phase 2)
- **Multi-shot** — Same as few-shot. (Phase 3)

## O
- **Opus** — Top intelligence tier. Slowest, most expensive. (Phase 1)
- **Orchestrator-workers** — Pattern: planner LLM splits work, workers run in parallel, planner synthesizes. (Phase 7)

## P
- **Parallel tool use** — A single response can contain multiple `tool_use` blocks. (Phase 4)
- **Prefilling** — Starting the assistant turn with text (`{`, `Step 1.`, …) to force format. (Phases 2, 3)
- **Prompt** (MCP) — Pre-canned named template user invokes (slash-command). (Phase 6)
- **Prompt caching** — See Cache control.
- **Prompt chaining** — Workflow pattern: fixed sequence of LLM calls. (Phase 7)
- **Prompt engineering** — The practice of writing prompts that reliably produce good outputs. (Phase 3)
- **Prompt injection** — Hostile instruction embedded in tool output / retrieved doc trying to override system prompt. (Phases 4, 5)

## R
- **RAG (Retrieval-Augmented Generation)** — Fetch relevant chunks → put in prompt → answer from them. (Phase 5)
- **ReAct** — Reason + Act loop. The de-facto autonomous-agent pattern. (Phase 7)
- **Reranking** — Cross-encoder scoring (q, doc) to refine top-k. (Phase 5)
- **Resource** (MCP) — App-/user-controlled data, identified by URI. (Phase 6)
- **Roles** — `system`, `user`, `assistant` in the Messages API. (Phase 2)
- **RRF (Reciprocal Rank Fusion)** — Score = Σ 1/(k + rank). Combines multiple ranked lists. (Phase 5)
- **Router workflow** — Pattern: classifier picks a downstream specialist. (Phase 7)

## S
- **Sectioning** — Parallel pattern: split task into independent subtasks. (Phase 7)
- **Sonnet** — Balanced tier; default for most production. (Phase 1)
- **`stop_reason`** — `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`. (Phase 2)
- **Streaming** — Receive output as deltas via `messages.stream()`. (Phase 2)
- **System prompt** — Top-level persona/rules. (Phase 2)
- **Subagent** — A separately-scoped Claude session spawned from Claude Code. (Phase 8)

## T
- **Temperature** — Sampling randomness. `0` = near-deterministic. (Phase 2)
- **Tool** — A function definition you give Claude. (Phase 4)
- **Tool use / `tool_use` block** — Claude's request to run a tool. (Phase 4)
- **Tool result / `tool_result` block** — Your reply containing the tool's output. (Phase 4)
- **`tool_choice`** — `auto` / `any` / `tool` / `none`. (Phase 4)
- **Transport (MCP)** — stdio vs Streamable HTTP. (Phase 6)

## V
- **Voting** — Parallel pattern: same task N times, majority answer wins. (Phase 7)

## W
- **Workflow** — System where YOU write the control flow. Prefer over agents when possible. (Phase 7)
- **`web_search` tool** — Server-side built-in tool. (Phase 4)

## X
- **XML tags** — Delimit prompt sections (`<task>`, `<context>`, `<example>`, `<answer>`). (Phase 3)
