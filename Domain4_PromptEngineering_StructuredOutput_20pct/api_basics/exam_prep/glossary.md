# Glossary — Domain 4a — Claude API basics (part of Domain 4, 20%)

Subset of the cross-domain glossary, filtered to terms tagged for this domain.


## `
- **`stop_reason`** — `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`. *(Phase 2)*

## B
- **Batch API** — Async bulk endpoint at ~50% discount. *(Phase 1)*

## C
- **Cache control / Prompt caching** — Mark content blocks with `cache_control: {type: 'ephemeral'}` to cache the prefix for 5 min; subsequent calls reuse it at ~10% cost. *(Phase 1, 5)*
- **Constitutional AI** — Anthropic's safety training technique (model critiques and revises itself against principles). *(Phase 1)*
- **Context window** — Maximum total tokens (input + output) per call. Up to 200K for current Claude. *(Phase 1)*

## E
- **Ephemeral cache** — 5-minute prompt cache TTL. *(Phase 1)*

## H
- **Haiku** — Smallest/fastest/cheapest Claude tier. *(Phase 1)*
- **Hallucination** — Confidently wrong output. Mitigations: RAG, tools, evals. *(Phase 1, 5)*

## J
- **Jailbreak** — Adversarial prompt designed to bypass safety. *(Phase 1)*
- **JSON Schema (`input_schema`)** — Structure for tool inputs (also for MCP). *(Phase 2, 4, 6)*

## M
- **Max tokens** — Cap on OUTPUT tokens per call. Must be set. *(Phase 2)*
- **Messages API** — Primary chat endpoint: `client.messages.create(...)`. *(Phase 2)*

## O
- **Opus** — Top intelligence tier. Slowest, most expensive. *(Phase 1)*

## P
- **Prefilling** — Starting the assistant turn with text (`{`, `Step 1.`, …) to force format. *(Phase 2, 3)*

## R
- **Roles** — `system`, `user`, `assistant` in the Messages API. *(Phase 2)*

## S
- **Sonnet** — Balanced tier; default for most production. *(Phase 1)*
- **Streaming** — Receive output as deltas via `messages.stream()`. *(Phase 2)*
- **System prompt** — Top-level persona/rules. *(Phase 2)*

## T
- **Temperature** — Sampling randomness. `0` = near-deterministic. *(Phase 2)*
