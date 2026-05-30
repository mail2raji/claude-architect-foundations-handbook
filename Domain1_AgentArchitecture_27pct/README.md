# Domain 1 — Agent Architecture & Orchestration

*Was Phase 7.* **Cert weight: 27% (the heaviest domain).**

**Maps to:** Skilljar "Agents and workflows" (11 lessons). **Exam weight: ~12%.**
**Goal:** Choose the right architecture for an autonomous Claude system and implement it.

> **Required reading before starting this phase:** Anthropic's essay **"Building effective agents"** — https://www.anthropic.com/research/building-effective-agents. The exam draws heavily from its taxonomy.

---

## Workflows vs Agents (the most important distinction in the exam)

| | Workflow | Agent |
|---|---|---|
| Control flow | **You** write the steps in code | **The model** decides next step in a loop |
| Predictability | High | Lower |
| Debuggability | Easier | Harder (must inspect agent trace) |
| Cost | Lower | Higher |
| When to use | You can enumerate the steps | The steps depend on inputs in ways you can't enumerate |

**Anthropic's official advice: prefer workflows. Reach for true agents only when the task is genuinely open-ended.**

---

## The 5 workflow patterns

### 1. Prompt chaining (sequential)
Step 1 → Step 2 → Step 3. Output of one feeds the next. Optional **gate** between steps validates before continuing.
Use: outline → draft → polish; translate → simplify → fact-check.
File: [`02_chain_workflow.py`](02_chain_workflow.py)

### 2. Routing
A "router" LLM call picks which of several specialists handles the input.
Use: support-ticket triage to billing/tech/refund specialists; model-tier routing (Haiku/Sonnet/Opus).
File: [`03_router_workflow.py`](03_router_workflow.py)

### 3. Parallelization
Same input fanned out to N parallel calls. Two flavors:
- **Sectioning** — split work into independent subtasks (chapters of a book).
- **Voting** — same task N times, majority/median vote (for reliability).
File: [`04_parallel_workflow.py`](04_parallel_workflow.py)

### 4. Orchestrator-workers
A central orchestrator LLM dynamically **plans** subtasks, spawns workers, then synthesizes.
Use: research deep-dives, code refactors across files.
Similar to parallelization but the *planner is also an LLM* — so the steps are dynamic.
File: [`05_orchestrator_workers.py`](05_orchestrator_workers.py)

### 5. Evaluator-optimizer (iterate-to-quality)
LLM A produces an output. LLM B critiques it. A revises. Repeat until B says "good enough".
Use: legal drafting, code generation with strict tests, marketing copy.
File: [`06_evaluator_optimizer.py`](06_evaluator_optimizer.py)

## The agent loop (true autonomy)

When workflows aren't enough, you give the model tools and let it loop:

```
while not done:
    action = LLM(state)        # decide next tool call
    if action == "finish": break
    observation = run_tool(action)
    state.append(observation)
```

This is **ReAct** (Reason + Act). Risks: looping forever, doing the wrong thing, racking up cost. Mitigations:

- **`max_steps` cap** (always)
- **Cost budget cap**
- **Logged trace** for debugging
- **Human approval** on dangerous actions (`tool_choice` gating, allow-list)
- **Sandboxing** (especially for `code_execution`, `computer_use`)

File: [`07_react_agent.py`](07_react_agent.py)

---

## Picking a pattern — decision flow

```
Is the task strictly enumerable in steps?  ─► YES ─► Chain workflow
                                              │
                                              NO
                                              │
Does input class drive different handling? ─► YES ─► Routing workflow
                                              │
                                              NO
                                              │
Can subtasks run in parallel?              ─► YES ─► Parallelization
                                              │
                                              NO
                                              │
Are subtasks dynamic / data-dependent?     ─► YES ─► Orchestrator-workers
                                              │
                                              NO
                                              │
Is quality strict, iterations help?        ─► YES ─► Evaluator-optimizer
                                              │
                                              NO
                                              │
Truly open-ended?                          ─► YES ─► Autonomous agent (ReAct)
```

---

## Real-world scenario

> **Document research agent.** A user asks: "What's the risk profile of vendor X based on our last 3 years of audit reports?"
>
> The right architecture mixes everything:
> - **Router** to pick "research mode".
> - **Orchestrator-workers** to plan sub-queries across years/topics.
> - Each worker uses **RAG (Phase 5)** + **tools (Phase 4)** via **MCP (Phase 6)**.
> - **Evaluator-optimizer** ensures the final summary cites sources.
>
> This is *the* exam scenario — be able to draw it on a whiteboard.

You build a compressed version in [`mini_project_research_agent.py`](mini_project_research_agent.py).

---

## Hands-on files

| # | File | Pattern |
|---|---|---|
| 1 | [`01_workflows_vs_agents.md`](01_workflows_vs_agents.md) | Cheat-sheet |
| 2 | [`02_chain_workflow.py`](02_chain_workflow.py) | Sequential w/ gate |
| 3 | [`03_router_workflow.py`](03_router_workflow.py) | Tier-routing Haiku/Sonnet/Opus |
| 4 | [`04_parallel_workflow.py`](04_parallel_workflow.py) | Sectioning + voting |
| 5 | [`05_orchestrator_workers.py`](05_orchestrator_workers.py) | Dynamic planner |
| 6 | [`06_evaluator_optimizer.py`](06_evaluator_optimizer.py) | Critique-and-revise |
| 7 | [`07_react_agent.py`](07_react_agent.py) | Autonomous loop w/ budget cap |
| 8 | [`mini_project_research_agent.py`](mini_project_research_agent.py) | Composed system |

---

## Exercises & mini quiz → [`exercises.md`](exercises.md)

Next → [Domain 2a: Tool Use (function calling)](../Domain2_ToolDesign_MCP_18pct/tool_use/README.md)
