# Domain 2 — Tool Design & MCP Integration

**Cert weight:** 18% of the Claude Certified Architect — Foundations exam.
**Goal:** Design tools Claude can call reliably, integrate them via the Model Context Protocol, and reason about tool selection, parallelism, structured errors, and security.

> This domain merges the original Phase 4 (Tool Use) and Phase 6 (MCP) modules. The folder layout is:
>
> - [`tool_use/`](tool_use/README.md) — the **client-side mechanics** of function calling: tool definitions, `tool_choice` modes, parallel/batch tool use, the agent loop.
> - [`mcp/`](mcp/README.md) — the **standard wire protocol**: MCP servers/clients, the three primitives (tools, resources, prompts), and bridging an MCP server to Claude.

Both subfolders are runnable end-to-end and are referenced by [LAB_GUIDE.md](../LAB_GUIDE.md) Domain 2 labs (2.1 – 2.7).

---

## What the exam expects you to be able to do

| Exam objective | Anchor file |
|---|---|
| Author tool definitions with clear, unambiguous descriptions | [`tool_use/01_function_calling.py`](tool_use/01_function_calling.py) |
| Distinguish `tool_choice` modes (`auto` / `any` / `tool` / `none`) | [`tool_use/01_function_calling.py`](tool_use/01_function_calling.py) |
| Drive the agent loop until `stop_reason != "tool_use"` | [`tool_use/02_multi_turn_tools.py`](tool_use/02_multi_turn_tools.py) |
| Issue & execute parallel tool calls | [`tool_use/03_parallel_tools.py`](tool_use/03_parallel_tools.py) |
| Return structured errors (`is_error: True` + machine-readable payload) | [`../Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py`](../Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py) |
| Build a custom IT/SOC tool agent | [`tool_use/04_it_triage_agent.py`](tool_use/04_it_triage_agent.py), [`mcp/mini_project_soc_mcp.py`](mcp/mini_project_soc_mcp.py) |
| Use built-in / server-side tools (`web_search`) | [`tool_use/05_builtin_web_search.py`](tool_use/05_builtin_web_search.py) |
| Recall the three MCP primitives and their owner | [`mcp/01_mcp_concepts.md`](mcp/01_mcp_concepts.md) |
| Build a stdio MCP server with `FastMCP` | [`mcp/02_mcp_server.py`](mcp/02_mcp_server.py) |
| Connect a client and call tools/resources programmatically | [`mcp/03_mcp_client.py`](mcp/03_mcp_client.py) |
| Bridge MCP tools into an Anthropic Messages call | [`mcp/04_bridge_mcp_to_claude.py`](mcp/04_bridge_mcp_to_claude.py) |

---

## The Tool ⇄ MCP relationship in one diagram

```
                           ┌────────────────────────────────────┐
                           │            CLAUDE MODEL            │
                           └────────────────────────────────────┘
                                    ▲              ▲
                                    │              │
       Anthropic Messages API ──────┘              └────────── Anthropic Messages API
       (your own `tools=[...]`)                              (auto-bridged from MCP)
                    │                                                │
            ┌───────┴────────┐                              ┌────────┴────────┐
            │  tool_use/     │                              │     mcp/        │
            │  custom tools  │                              │  bridge layer   │
            │  you wrote     │                              │  (04_bridge_…)  │
            └────────────────┘                              └────────┬────────┘
                                                                     │
                                                          ┌──────────┴──────────┐
                                                          │     MCP SERVERS     │
                                                          │  (Phase 6 + 3rd-    │
                                                          │   party + Claude    │
                                                          │   Desktop installs) │
                                                          └─────────────────────┘
```

`tool_use/` teaches the **invocation surface** (Anthropic Messages tool calling).
`mcp/` teaches the **distribution surface** (publish those tools so any client can plug in).
Production agents almost always do **both**.

---

## Recommended order

1. Read this README.
2. Work through [`tool_use/README.md`](tool_use/README.md) and run files 01 → 05.
3. Do the [`tool_use/exercises.md`](tool_use/exercises.md).
4. Move to [`mcp/README.md`](mcp/README.md), run files 01 → 04, then the mini-project.
5. Do the [`mcp/exercises.md`](mcp/exercises.md).
6. Return to [LAB_GUIDE.md](../LAB_GUIDE.md) Domain 2 labs for the synthesis exercises (similar-tool selection, interceptor hooks, etc.) — most are anchored on [`../Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py`](../Domain1_AgentArchitecture_27pct/08_agent_loop_with_escalation.py).

---

Next → [Domain 5 — Context Management & Reliability](../Domain5_ContextMgmt_Reliability_15pct/README.md)
