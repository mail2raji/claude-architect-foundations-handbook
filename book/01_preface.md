# Preface

## Why this book exists

The official Anthropic Skilljar courses ("Building with the Claude API", "Introduction to Model Context Protocol", "Claude Code in Action") are excellent. They are the canonical source for the Claude Certified Architect Foundations exam.

But three things make a learner stall:

1. **Scattered**. The exam blueprint is spread across multiple free courses and a research essay.
2. **Toy-shaped**. Most public tutorials use cute examples (cats, weather) that don't transfer to the regulated, real-world environments you actually build for.
3. **Missing the architect's perspective**. Knowing the API isn't the same as choosing the right *pattern* under cost, latency, safety, and compliance constraints. That's what the exam — and your job — actually test.

This book exists to bridge that gap. It is:

- **Hands-on.** Every concept ships with runnable Python you can execute on your laptop with one API key.
- **Real-world.** Every example uses scenarios you would meet in an IT, security, banking, or healthcare environment: SOC alert triage, compliance Q&A, MFA reset, GDPR breach notification, code review.
- **Architect-shaped.** Every phase ends with "when do you choose this pattern?" and "what goes wrong in production?", so by the end you can defend a design, not just code one.
- **Exam-aligned.** The 11-phase structure maps 1:1 to the public Skilljar course blueprint plus the deeper architectural material the exam tests but the free courses don't fully cover.

## Who this book is for

- You are new to Claude and possibly to generative AI overall.
- You can read basic Python; you do *not* need a machine-learning background.
- You want to take and pass the **Claude Certified Architect Foundations** exam with confidence.
- You also want to be able to ship the systems it tests in production at work.

If you already work in IT, security, or platform engineering, you will recognize the example scenarios immediately. If you don't, the scenarios are explained from first principles.

## How to read this book

1. Start at **Chapter 1 (Setup)** and run the first API call.
2. Read each chapter end-to-end before opening the code.
3. Run every code sample. *Reading without running is the #1 cause of low exam scores.*
4. Do the exercises at the end of each chapter.
5. After Chapter 10 (Exam Prep), take the three mock exams under timed conditions.
6. After Chapter 11 (Advanced Capstone), sketch answers to the 25 architecture problems.

Estimated effort: 30–60 hours of focused practice. There is no fixed schedule; go at your own pace.

## What you will be able to do at the end

- Call Claude via the Anthropic API for chat, streaming, vision, and structured JSON.
- Write production-grade prompts and evaluate them systematically.
- Build Claude apps that use tools (function calling).
- Build a RAG pipeline with chunking, embeddings, hybrid retrieval, reranking, and contextual retrieval.
- Build and consume MCP (Model Context Protocol) servers and clients.
- Design agents and workflows — chain, router, parallelization, orchestrator-workers, evaluator-optimizer, ReAct.
- Use Claude Code and understand Computer Use risks.
- Pass the Claude Certified Architect Foundations exam.
- Defend the architecture you chose, with cost / latency / safety arguments.

## Conventions

- Code blocks use Python and are runnable as-is once `ANTHROPIC_API_KEY` is set.
- Real-world scenarios are introduced in *italics* before the technique.
- The "**Gotcha**" callout marks a common production bug or exam trap.
- The "**Pattern**" callout marks an architectural decision to memorize.
- All model names — `claude-haiku-4-5`, `claude-sonnet-4-5`, `claude-opus-4-5` — are the names current as of this edition. If Anthropic ships newer model strings while you study, update them in the code.

## A note on honesty

This book does not pretend that LLMs are magic. The exam tests when you should *not* reach for an LLM (e.g., 200 ms p99 fraud scoring), when a simple workflow beats an autonomous agent (almost always), and when the right answer is "I don't know — measure it." So does this book.

Let's get started.
