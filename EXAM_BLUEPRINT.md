# Claude Certified Architect Foundations — Exam Blueprint

This blueprint is derived from the official Anthropic **"Building with the Claude API"** and **"Introduction to MCP"** Skilljar courses (the public, free curriculum that the Foundations certification is built around). Use it as your study scope and self-grading rubric.

## Exam-style domains and weighting (recommended study weight)

| # | Domain | Weight | Phase covering it |
|---|---|---:|---|
| 1 | Claude models, pricing, and platform fundamentals | 8% | Phase 1 |
| 2 | Claude API: messages, roles, system prompts, streaming, vision, structured output | 15% | Phase 2 |
| 3 | Prompt engineering (XML tags, CoT, prefilling, few-shot, role prompting) | 14% | Phase 3 |
| 4 | Prompt evaluation (LLM-as-judge, ground truth, automated test pipelines) | 8% | Phase 3 |
| 5 | Tool use / function calling (single, multi-turn, parallel/batch, errors) | 15% | Phase 4 |
| 6 | RAG (chunking, embeddings, BM25 hybrid, reranking, contextual retrieval) | 12% | Phase 5 |
| 7 | Model Context Protocol (servers, clients, tools, resources, prompts) | 10% | Phase 6 |
| 8 | Agents & workflows (router, parallel, chain, evaluator-optimizer, ReAct) | 12% | Phase 7 |
| 9 | Claude Code & Computer Use awareness | 3% | Phase 8 |
| 10 | Safety, responsible AI, system constraints (hallucination, jailbreaks, limits) | 3% | Phases 1, 3, 7 |

> Weights are *guidance* (not published numbers). Each Phase README has a "Exam tips" callout flagging the highest-yield items.

## Format expectations (typical Anthropic Skilljar quizzes)

- Multiple-choice / multi-select
- Scenario-based questions ("which architecture would you choose…")
- Short code-reading questions (identify the bug or the correct API parameter)
- No live coding during the exam

## Self-readiness checklist

You are ready to sit the exam when you can answer **yes** to all of these without notes:

- [ ] I can name the current Claude model families and the key trade-offs (speed vs. intelligence vs. cost).
- [ ] I can write a Python call to `client.messages.create(...)` from memory including `system`, `messages`, `max_tokens`, `temperature`.
- [ ] I can stream a response and consume `event` deltas.
- [ ] I can extract structured JSON from Claude using prefilling AND tool use, and explain when to pick each.
- [ ] I can write a prompt using `<task>`, `<context>`, `<example>` XML tags and explain why XML helps Claude.
- [ ] I can implement a basic LLM-as-judge eval loop.
- [ ] I can register a tool (`tools=[…]`), parse `tool_use` blocks, and reply with `tool_result` blocks.
- [ ] I can describe the difference between **tools**, **resources**, and **prompts** in MCP.
- [ ] I can sketch an MCP server (`@mcp.tool()`) and an MCP client connecting over stdio.
- [ ] I can name 4+ agent workflow patterns (router, parallelization, chaining, evaluator-optimizer, orchestrator-workers, autonomous agent) and pick one for a given scenario.
- [ ] I can implement contextual retrieval and explain why it improves recall over plain RAG.
- [ ] I know when to use a workflow vs. a true autonomous agent.

When 12 of 12 are checked, take the exam.

## Mapping back to the Skilljar curriculum

| Skilljar section | Lessons | Phase here |
|---|---:|---|
| Getting started with Claude | 16 | Phase 2 |
| Prompt engineering & evaluation | 16 | Phase 3 |
| Tool use with Claude | 14 | Phase 4 |
| Retrieval augmented generation | 10 | Phase 5 |
| Model Context Protocol (MCP) | 12 | Phase 6 |
| Claude Code & Computer Use | 8 | Phase 8 |
| Agents and workflows | 11 | Phase 7 |
| MCP fundamentals & server development | 8 | Phase 6 |
| MCP client implementation & advanced features | 8 | Phase 6 |
