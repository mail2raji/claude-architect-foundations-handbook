# How to use this handbook

You have three modes available:

## Mode 1 — Read the book

Open [`BOOK.md`](../BOOK.md) and read it cover-to-cover on GitHub. Every chapter is rendered with full markdown, code, and links.

## Mode 2 — Run the chapters

Each chapter has its own folder. The pre-domain modules keep their `Phase*` names ([`Phase0_Setup/`](../Phase0_Setup/README.md), [`Phase1_Foundations/`](../Phase1_Foundations/README.md)), the five exam-domain modules use `Domain*` names (see layout below), and exam prep + capstone keep their `Phase*` names. Each folder contains a chapter README, runnable `*.py` files, and (usually) an `exercises.md`.

## Mode 3 — Treat it as exam prep

Skip to [`Phase9_ExamPrep/`](../Phase9_ExamPrep/README.md) for glossary, three mock exams (90 questions total), and a per-domain checklist. Then deepen with [`Phase10_Advanced_Capstone/`](../Phase10_Advanced_Capstone/README.md). Also see [`LAB_GUIDE.md`](../LAB_GUIDE.md) for a full domain-by-domain lab walkthrough.

## Required setup

1. Create an Anthropic account and an API key (begins with `sk-ant-`). See [`SETUP.md`](../SETUP.md).
2. (Optional but recommended for Chapter 6) Get a Voyage AI key for embeddings + reranking.
3. Install Python 3.10+, create a venv, `pip install -r requirements.txt`.
4. Copy `.env.example` → `.env` and paste your keys.

## Estimated cost

If you run every code sample once, the total Anthropic spend is typically under **USD $5**. Add up to **USD $2** for Voyage if you run the RAG chapters. You can run the entire book on a free Anthropic developer tier for most chapters.

## Repository layout

```
.
├── BOOK.md                       single-file book (auto-generated)
├── README.md                     repo landing page
├── SETUP.md                      environment setup
├── EXAM_BLUEPRINT.md             exam domain weights & checklist
├── LAB_GUIDE.md                  domain-by-domain hands-on labs
├── requirements.txt
├── book/                         book front matter (preface, etc.)
├── Phase0_Setup/                                              Chapter 1  (pre-domain)
├── Phase1_Foundations/                                        Chapter 2  (pre-domain)
├── Domain4_PromptEngineering_StructuredOutput_20pct/          Chapters 3–4  (Domain 4, 20%)
│   ├── api_basics/
│   └── prompt_engineering/
├── Domain2_ToolDesign_MCP_18pct/                              Chapters 5 & 7  (Domain 2, 18%)
│   ├── tool_use/
│   └── mcp/
├── Domain5_ContextMgmt_Reliability_15pct/                     Chapter 6  (Domain 5, 15%)
├── Domain1_AgentArchitecture_27pct/                           Chapter 8  (Domain 1, 27%)
├── Domain3_ClaudeCode_Workflows_20pct/                        Chapter 9  (Domain 3, 20%)
├── Phase9_ExamPrep/                                           Appendix A
├── Phase10_Advanced_Capstone/                                 Appendix B
└── tools/                        BOOK.md & mdbook builder scripts
```
