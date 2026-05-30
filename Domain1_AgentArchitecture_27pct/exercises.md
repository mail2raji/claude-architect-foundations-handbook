# Phase 7 — Exercises

1. Take a real PowerShell task you do at work (e.g. "find SPNs about to expire"). Sketch which pattern fits — chain, router, parallel, orchestrator, evaluator-optimizer, or autonomous? Write one paragraph justification.
2. In `07_react_agent.py`, add a `max_cost_usd` budget that estimates token cost per step (use approximate per-million prices) and stops when exceeded.
3. Improve `06_evaluator_optimizer.py`: instead of one critic, run **three judges in parallel** and average their scores. Did quality improve?
4. Combine Phase 4 (tools), Phase 5 (RAG), Phase 6 (MCP), Phase 7 (orchestrator). Picture a real assistant for your team. Sketch the diagram.

## Mini quiz

1. When should you prefer a workflow over an agent?
2. Two flavors of parallelization?
3. What's the difference between an orchestrator-workers pattern and a chain?
4. Name three safety knobs every autonomous agent must have.
5. What pattern is "draft → critique → revise → repeat until rubric pass"?

### Answers
1. Whenever you can enumerate the steps and want predictability/cost control.
2. **Sectioning** (split-into-subtasks) and **voting** (same task N times).
3. In a chain, the steps are hardcoded by you. In orchestrator-workers, a planning LLM decides the steps at runtime.
4. `max_steps`, cost budget, tool allow-list (any others: sandboxing, human-in-loop for irreversible ops, trace logging).
5. **Evaluator-optimizer**.
