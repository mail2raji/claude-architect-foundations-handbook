# Phase 10 — Advanced Capstone

This phase exists because **the exam will test architecture decisions, not API trivia**. Anyone can memorize `client.messages.create`. What separates a passing score from a high score is recognizing when to use which pattern under realistic constraints (cost, latency, safety, compliance).

Five capstones modeled after real engineering tickets you'd see in a regulated enterprise (NFCU/IT/Sec context).

## Files

| # | Project | What it teaches | File |
|---|---|---|---|
| 1 | SOC Alert Triage Pipeline | Router → tool agent → MCP → eval | [`01_soc_triage_pipeline.py`](01_soc_triage_pipeline.py) |
| 2 | Compliance Document Q&A with attribution | Production RAG: hybrid + rerank + contextual + caching | [`02_compliance_rag_production.py`](02_compliance_rag_production.py) |
| 3 | Multi-tier customer support agent | Routing + tools + escalation + observability | [`03_support_agent_multi_tier.py`](03_support_agent_multi_tier.py) |
| 4 | Code-review autonomous agent (sandboxed) | ReAct + filesystem tools + budget guards | [`04_code_review_agent.py`](04_code_review_agent.py) |
| 5 | Enterprise eval harness | Eval suite + regression tracking + LLM-judge | [`05_eval_harness.py`](05_eval_harness.py) |
| — | **Architectural decision cheat-sheet** | When to pick what | [`patterns_decision_tree.md`](patterns_decision_tree.md) |
| — | **Common pitfalls / gotchas** | Real bugs people ship | [`gotchas.md`](gotchas.md) |
| — | **Production cost & latency cheat-sheet** | Bill-killers and how to fix | [`production_cheatsheet.md`](production_cheatsheet.md) |
| — | **Advanced scenario exercises** | 25 architectural sketches | [`advanced_exercises.md`](advanced_exercises.md) |
| — | **Harder per-phase exercises** | Stretch problems for Phases 2–8 | [`harder_exercises_by_phase.md`](harder_exercises_by_phase.md) |

## How to use this phase

1. **Read** [`patterns_decision_tree.md`](patterns_decision_tree.md), [`gotchas.md`](gotchas.md), [`production_cheatsheet.md`](production_cheatsheet.md).
2. **Run** capstones 1–5 with your own API key.
3. **Sketch** answers to all 25 problems in [`advanced_exercises.md`](advanced_exercises.md). Compare to the solution sketches at the bottom.
4. **Take** the Set C mock exam in [`../Phase9_ExamPrep/practice_questions_setC.md`](../Phase9_ExamPrep/practice_questions_setC.md).

If you can do all of the above without notes, you are exam-ready with a margin.
