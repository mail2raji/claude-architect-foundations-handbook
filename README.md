# Claude Certified Architect Foundations — The Hands-On Handbook

> *From zero to production-grade agents — and a confident pass on the exam.*

A complete, hands-on, real-world **book + repository** to learn **Claude (by Anthropic)** for **GenAI** and **Agentic AI**, structured so you can confidently take the **Claude Certified Architect Foundations** exam on `anthropic.skilljar.com`.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status](https://img.shields.io/badge/edition-1.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

---

## Read the book

- **Single-file book**: [BOOK.md](BOOK.md) — all 7 chapters + 7 per-domain appendices in one navigable file.
- **Chapter-by-chapter**: pick a domain folder from the table below.
- **Just exam prep**: every domain folder has its own `exam_prep/` subfolder — start with the heaviest, [Domain 1 (27%)](Domain1_AgentArchitecture_27pct/exam_prep/).

> The Foundations exam aligns to Anthropic's free **"Building with the Claude API"** course. This handbook mirrors that exam blueprint exactly, plus prerequisite GenAI foundations and an advanced capstone the official course doesn't fully cover.

---

## Who this is for

- You are **new to Claude** (and possibly to GenAI / Agentic AI).
- You want to go from **zero → Architect Foundations exam-ready**.
- You prefer **real-world examples** (IT operations, document Q&A, IT triage agent, etc.) over toy demos.
- You can read basic Python. You don't need ML or data-science background.

## What you will be able to do at the end

1. Call Claude via the Anthropic API for chat, streaming, vision, and structured JSON.
2. Write production-grade prompts and **evaluate** them systematically.
3. Build Claude apps that **use tools** (function calling).
4. Build a **RAG** pipeline (chunking → embeddings → BM25 hybrid → reranking → contextual retrieval).
5. Build and consume **MCP** (Model Context Protocol) servers and clients.
6. Design **agents and workflows** (router, parallel, evaluator-optimizer, ReAct loop).
7. Use **Claude Code** and understand **Computer Use**.
8. **Pass the Claude Certified Architect Foundations exam**.

---

## Learning Roadmap (organised by exam domain)

The Claude Certified Architect — Foundations exam has five domains with the following weights. All foundations, setup, exam prep, and capstone content lives **inside the relevant domain folder** so each domain is a self-contained study unit.

| Order | Module | Maps to exam domain | Cert weight | Folder |
|---|---|---|---|---|
| 1 | Foundations, setup, & the Claude API | **Domain 4** — Prompt Engineering & Structured Output | 20% | [Domain4_…/api_basics/](Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/README.md) |
| 2 | Prompt Engineering & Evaluation | **Domain 4** — Prompt Engineering & Structured Output | 20% | [Domain4_…/prompt_engineering/](Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering/README.md) |
| 3 | Tool Use (Function Calling) | **Domain 2** — Tool Design & MCP Integration | 18% | [Domain2_…/tool_use/](Domain2_ToolDesign_MCP_18pct/tool_use/README.md) |
| 4 | Retrieval Augmented Generation | **Domain 5** — Context Management & Reliability | 15% | [Domain5_ContextMgmt_Reliability_15pct/](Domain5_ContextMgmt_Reliability_15pct/README.md) |
| 5 | Model Context Protocol (MCP) | **Domain 2** — Tool Design & MCP Integration | 18% | [Domain2_…/mcp/](Domain2_ToolDesign_MCP_18pct/mcp/README.md) |
| 6 | Agents & Workflows | **Domain 1** — Agent Architecture & Orchestration | 27% | [Domain1_AgentArchitecture_27pct/](Domain1_AgentArchitecture_27pct/README.md) |
| 7 | Claude Code & Computer Use | **Domain 3** — Claude Code Configuration & Workflows | 20% | [Domain3_ClaudeCode_Workflows_20pct/](Domain3_ClaudeCode_Workflows_20pct/README.md) |

> See [LAB_GUIDE.md](LAB_GUIDE.md) for the domain-by-domain hands-on lab walkthrough that combines these modules into exam-style scenarios.

Each **domain folder** contains:
- `README.md` — concepts, diagrams, real-world scenarios, examples, exercises
- `*.py` — runnable code samples for each sub-topic
- `lab_walkthrough.py` — **one** step-by-step lab that walks the whole domain end to end
- `exercises.md` — try-it-yourself drills
- `exam_prep/` — this domain's slice of the glossary, practice questions (Sets A+B and Set C), harder exercises, and architectural scenarios
- `capstones/` (where applicable) — production-shaped projects tagged to this domain

---

## Suggested pace (no time pressure — go at your own speed)

Study domain-by-domain, in **exam-weight order** so you cover the heaviest domains first:

1. **Domain 1 (27%)** — Agent architecture. Read README, run `lab_walkthrough.py`, then 02–08 scripts, then the `capstones/`.
2. **Domain 4 (20%)** — Foundations + API + prompt engineering. The `api_basics/` sub-folder doubles as your entry point if you've never made a Claude call.
3. **Domain 3 (20%)** — Claude Code & workflows.
4. **Domain 2 (18%)** — Tool use + MCP (two sub-folders).
5. **Domain 5 (15%)** — RAG + context management + reliability.

For each domain: README → `lab_walkthrough.py` → numbered `*.py` files → `exercises.md` → `exam_prep/` (glossary, checklist, practice questions, harder exercises, scenarios).

Tip: After each domain, write a 5-line "what I learned" note in [study_notes.md](study_notes.md). The act of summarizing locks in retention.

---

## How confident will I be on exam day?

Honest answer based on how far you go:

| If you complete | Expected exam result |
|---|---|
| Only the domain READMEs (read, don't run code) | ~50% — you'll know vocabulary but get tripped by scenarios |
| Every domain README + every `lab_walkthrough.py` + every `exam_prep/practice_questions.md` (≥ 85%) | Likely pass with comfortable margin |
| Above + every `capstones/` script + every `exam_prep/practice_questions_setC.md` (≥ 80%) | High-confidence pass; you can design real systems, not just answer trivia |

If you only have time for the minimum, do every domain's `lab_walkthrough.py` and `exam_prep/final_checklist.md`, plus [`Domain1_…/patterns_decision_tree.md`](Domain1_AgentArchitecture_27pct/patterns_decision_tree.md) and [`Domain1_…/gotchas.md`](Domain1_AgentArchitecture_27pct/gotchas.md) — these cover the most common exam traps.

---

## How to start

1. Read [SETUP.md](SETUP.md) and get an Anthropic API key.
2. Install dependencies → `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` and paste your `ANTHROPIC_API_KEY`.
4. Run `python Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/00_setup_first_call.py` — if you see Claude reply, you're ready.
5. Open [Domain4_…/api_basics/00_foundations.md](Domain4_PromptEngineering_StructuredOutput_20pct/api_basics/00_foundations.md) and begin.

---

## Related official resources (free)

- Course: **Building with the Claude API** — https://anthropic.skilljar.com/claude-with-the-anthropic-api
- Course: **Introduction to Model Context Protocol** — https://anthropic.skilljar.com/introduction-to-model-context-protocol
- Course: **Claude Code in Action** — https://anthropic.skilljar.com/claude-code-in-action
- Anthropic API docs — https://docs.anthropic.com
- Anthropic Cookbook — https://github.com/anthropics/anthropic-cookbook
- Anthropic "Building effective agents" essay — https://www.anthropic.com/research/building-effective-agents

> If `claude-certified-architect-foundations` becomes a public Skilljar URL while you're studying, complete that course at the end as your final review. The blueprint in [EXAM_BLUEPRINT.md](EXAM_BLUEPRINT.md) is built from the same skill domains.

---

## Stats

- 11 phases / 9 chapters + 2 appendices
- 75+ files of curriculum
- 30+ runnable Python examples
- 90 mock-exam questions across 3 sets, plus 25 architecture exercises
- 5 production-grade capstone projects

## Regenerating the single-file book

After editing any chapter, regenerate [BOOK.md](BOOK.md):

```powershell
python tools/build_book.py
```

## License

MIT — see [LICENSE](LICENSE). The book text and code are both MIT.

Good luck — let's get you certified.
