# Harder Exercises — Domain 1 — Agent Architecture & Orchestration (27%)

Subset of the cross-domain 'harder exercises' file, filtered to this domain.
Each exercise expects an architect-level answer, not a tutorial-follower answer.

## (was Phase 7) Agents (harder)


**7H-1.** Take a workflow that solves a problem at $0.20/call. Refactor it to an autonomous agent. Measure cost and success rate. When is the agent worth it?

**7H-2.** Build the orchestrator-workers pattern across 5 workers running in parallel. Add a watchdog: if any worker fails twice, the orchestrator retries with a different model.

**7H-3.** Build evaluator-optimizer with a stop condition that says "stop if score has not improved for 2 rounds" (early stopping). Measure rounds-to-converge across 20 inputs.

**7H-4.** Build a ReAct agent with **three** safety knobs: max_steps, token budget, tool allow-list per step. Demonstrate each kicking in.

**7H-5.** Build voting with 5 voters and measure the calibration of vote-share to correctness (does 4/5 votes mean 80% accuracy?).

---

## Cross-phase harder problems

**X-1.** A team built a chatbot with: Sonnet, no caching, 50K-token static system prompt, `temperature=0.7`, no `max_steps`, no tool allow-list, free-form JSON instruction. List EVERY problem in priority order and propose fixes.

**X-2.** Design a per-call "system meter": prints cost-per-call, p50/p99 latency, cache hit rate, top-3 tools called, error rate. Use it on a small workload.

**X-3.** Build a regression suite that locks down a chatbot's behavior with 50 golden cases. When you upgrade the model snapshot, you should see the diff.

---


## Hints (skim if stuck)

- **2H-2:** Use `with client.messages.stream(...)` and break out of the for-loop when you detect the trigger; cancel via `stream.close()`.
- **2H-4:** Tool-use-as-formatter wins. Prefilling sometimes drifts on long inputs. Plain instruction is the least reliable.
- **3H-2:** Layering helps. The "data not instructions" rule alone catches ~60% of injections; combined with XML wrappers it catches ~90%.
- **4H-1:** `any` forces a tool call which means the model can pick a wrong tool to satisfy the constraint. Use `auto` unless you genuinely require a call.
- **5H-1:** Vector wins on semantic queries; BM25 wins on exact-token queries; hybrid wins on both; reranker wins on the top-1 reordering.
- **5H-5:** Query rewriting typically adds 5–15% recall. Beware: it costs N extra retrievals.
- **6H-3:** Sampling is the trickiest MCP capability. Server defines, client implements, client's model does the work.
- **7H-3:** Common stopping rule: `if score >= 4 OR rounds == 3 OR no_improvement_count >= 2: stop`.
- **X-1:** In order: no `max_steps`, no allow-list, no caching, JSON via instruction (use tool), temperature too high, no observability.
