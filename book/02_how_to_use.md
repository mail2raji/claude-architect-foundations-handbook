# How to use this handbook

You have three modes available:

## Mode 1 — Read the book

Open [`BOOK.md`](../BOOK.md) and read it cover-to-cover on GitHub. Every chapter is rendered with full markdown, code, and links.

## Mode 2 — Run the chapters

Each chapter has its own folder ([`Phase0_Setup/`](../Phase0_Setup/README.md), [`Phase1_Foundations/`](../Phase1_Foundations/README.md), …) with a chapter README, runnable `*.py` files, and an `exercises.md`. Clone the repo, set up the environment, run each sample.

## Mode 3 — Treat it as exam prep

Skip to [`Phase9_ExamPrep/`](../Phase9_ExamPrep/README.md) for glossary, three mock exams (90 questions total), and a per-phase checklist. Then deepen with [`Phase10_Advanced_Capstone/`](../Phase10_Advanced_Capstone/README.md).

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
├── requirements.txt
├── book/                         book front matter (preface, etc.)
├── Phase0_Setup/                 Chapter 1
├── Phase1_Foundations/           Chapter 2
├── Phase2_API_Basics/            Chapter 3
├── Phase3_Prompt_Engineering/    Chapter 4
├── Phase4_Tool_Use/              Chapter 5
├── Phase5_RAG/                   Chapter 6
├── Phase6_MCP/                   Chapter 7
├── Phase7_Agentic_AI/            Chapter 8
├── Phase8_Claude_Code_Computer_Use/  Chapter 9
├── Phase9_ExamPrep/              Chapter 10 (Appendix A)
├── Phase10_Advanced_Capstone/    Chapter 11 (Appendix B)
└── tools/                        BOOK.md builder script
```
