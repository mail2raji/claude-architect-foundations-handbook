# Final Readiness Checklist

Tick each box only when you can do it WITHOUT notes.

## Phase 1 — Foundations
- [ ] I can name the three Claude tiers and pick one for a given task.
- [ ] I can state the current production context window (200K tokens).
- [ ] I can explain why input tokens usually dominate cost.

## Phase 2 — API
- [ ] I can write `client.messages.create(...)` from memory: `model`, `max_tokens`, `system`, `messages`, `temperature`.
- [ ] I can describe each `stop_reason`.
- [ ] I can produce strict JSON two different ways (prefill + tool-as-formatter).

## Phase 3 — Prompting & Eval
- [ ] I can explain XML tags and why Claude respects them.
- [ ] I can use `<thinking>` + `<answer>` and extract the answer.
- [ ] I can build a ground-truth eval AND an LLM-as-judge eval.

## Phase 4 — Tools
- [ ] I can write the agent loop (assistant turn with `tool_use` → user turn with `tool_result`) on a whiteboard.
- [ ] I can describe each `tool_choice` mode.
- [ ] I can defend against prompt injection via tool output.

## Phase 5 — RAG
- [ ] I can describe the 5-stage pipeline.
- [ ] I can explain why hybrid + rerank beats pure vector.
- [ ] I can explain Anthropic's contextual retrieval.

## Phase 6 — MCP
- [ ] I can state the three primitives and who controls each.
- [ ] I can name the two transports.
- [ ] I can sketch a minimal MCP server in Python from memory.

## Phase 7 — Agents
- [ ] I can name 5 workflow patterns and pick one for a scenario.
- [ ] I can articulate when to use a workflow vs an autonomous agent.
- [ ] I can list three safety knobs every agent must have.

## Phase 8 — Claude Code & Computer Use
- [ ] I can describe what Claude Code is, in one sentence.
- [ ] I can describe Computer Use's risks.

## Practice scores
- [ ] Set A score: ___ / 30
- [ ] Set B score: ___ / 30

## Logistics
- [ ] I know how to access the exam (Skilljar account).
- [ ] I have a stable internet connection and a quiet 90 minutes.
- [ ] I will read every question twice.

When every box is ticked → schedule the exam.
