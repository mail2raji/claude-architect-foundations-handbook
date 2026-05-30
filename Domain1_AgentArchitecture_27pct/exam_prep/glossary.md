# Glossary — Domain 1 — Agent Architecture & Orchestration (27%)

Subset of the cross-domain glossary, filtered to terms tagged for this domain.


## A
- **Agent** — A loop where the model decides the next tool call based on observations until done. *(Phase 7)*
- **Allow-list (tools)** — Restricting which tools an agent may call at a given step. Safety knob. *(Phase 7)*

## E
- **Evaluator-optimizer** — Generator-and-critic loop until rubric passes. *(Phase 7)*

## G
- **Gate** — A conditional check between workflow steps. *(Phase 7)*

## M
- **Max steps** — Cap on agent loop iterations. Required safety knob. *(Phase 7)*

## O
- **Orchestrator-workers** — Pattern: planner LLM splits work, workers run in parallel, planner synthesizes. *(Phase 7)*

## P
- **Prompt chaining** — Workflow pattern: fixed sequence of LLM calls. *(Phase 7)*

## R
- **ReAct** — Reason + Act loop. The de-facto autonomous-agent pattern. *(Phase 7)*
- **Router workflow** — Pattern: classifier picks a downstream specialist. *(Phase 7)*

## S
- **Sectioning** — Parallel pattern: split task into independent subtasks. *(Phase 7)*

## V
- **Voting** — Parallel pattern: same task N times, majority answer wins. *(Phase 7)*

## W
- **Workflow** — System where YOU write the control flow. Prefer over agents when possible. *(Phase 7)*
