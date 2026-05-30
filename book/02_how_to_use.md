# How to use this handbook

You have three modes available:

## Mode 1 — Read the book

Open [`BOOK.md`](../BOOK.md) and read it cover-to-cover on GitHub. Every chapter is rendered with full markdown, code, and links.

## Mode 2 — Run the chapters

Each chapter has its own folder named after the exam domain it covers (`Domain1_AgentArchitecture_27pct/`, `Domain2_ToolDesign_MCP_18pct/`, …). Every domain folder contains a chapter README, runnable `*.py` files, an `exercises.md`, a single `lab_walkthrough.py` step-by-step lab, and an `exam_prep/` subfolder with that domain's slice of the glossary, checklist, practice questions, and harder exercises.

## Mode 3 — Treat it as exam prep

Each domain ships its own `exam_prep/` folder with a glossary, final checklist, practice questions (Sets A+B and Set C), harder exercises, and architectural scenarios — all filtered to just that domain. Drill the heaviest domain first ([`Domain1_AgentArchitecture_27pct/exam_prep/`](../Domain1_AgentArchitecture_27pct/exam_prep/), 27%), then work down. Also see [`LAB_GUIDE.md`](../LAB_GUIDE.md) for a full domain-by-domain lab walkthrough.

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
├── Domain1_AgentArchitecture_27pct/                           Chapter 6  (Domain 1, 27% — heaviest)
│   ├── exam_prep/                                              per-domain exam prep
│   ├── capstones/                                              capstones tagged to Domain 1
│   └── lab_walkthrough.py                                      single step-by-step lab
├── Domain2_ToolDesign_MCP_18pct/                              Chapters 3 & 5  (Domain 2, 18%)
│   ├── tool_use/  (incl. exam_prep/)
│   ├── mcp/       (incl. exam_prep/)
│   └── lab_walkthrough.py
├── Domain3_ClaudeCode_Workflows_20pct/                        Chapter 7  (Domain 3, 20%)
│   ├── exam_prep/
│   └── lab_walkthrough.py
├── Domain4_PromptEngineering_StructuredOutput_20pct/          Chapters 1–2  (Domain 4, 20%)
│   ├── api_basics/ (foundations + setup live here, incl. exam_prep/)
│   ├── prompt_engineering/ (incl. exam_prep/)
│   └── lab_walkthrough.py
├── Domain5_ContextMgmt_Reliability_15pct/                     Chapter 4  (Domain 5, 15%)
│   ├── exam_prep/
│   └── lab_walkthrough.py
└── tools/                        BOOK.md & mdbook builder scripts
```
