# Advanced Architectural Scenarios — Domain 5 — Context Management & Reliability (15%)

Sourced from the consolidated 25 cross-domain scenarios.
Only the **4 scenarios tagged for this domain** appear here.

Sketch an architecture answer first, then compare to the solution sketch at the bottom.

---

## Exercises

**E1.** A regional credit union wants a chatbot over its 1,200-page member handbook. Members ask things like "What's the penalty for early CD withdrawal?". Latency SLA is < 4s. Design the system.

**E6.** A hospital deploys an internal Q&A bot over 40K policy documents. PHI must NEVER leave the EU. Architect.

**E22.** A RAG bot answers "I don't know" to questions whose answer is clearly in the corpus. Diagnose.

**E23.** Same RAG bot occasionally hallucinates facts not in the corpus. Diagnose.


---
## Solution sketches

**A1.** Hybrid RAG (vector + BM25 for "Section 4.2"-style queries) + reranker → top-5 chunks → Sonnet with citations. Index once. Per query: embed → search → rerank → answer. Latency budget: < 200ms retrieval, < 2s Sonnet → fits 4s SLA. Cache the system prompt + retrieval rules.

**A6.** Self-hosted inference cluster in EU region (Bedrock/Vertex EU regions or on-prem). Hybrid RAG. **Never** call public API. Audit log of every retrieval hit. Anonymize PHI in any embedding-side telemetry.

**A22.** Retrieval is missing the doc. Diagnose: (a) chunk size too small/large, (b) embeddings don't capture acronyms — add BM25, (c) missing contextual prefixes, (d) reranker is rejecting it. Add eval cases for each failed query.

**A23.** System prompt isn't strict enough. Add: "Answer ONLY from the chunks in `<context>`. If absent, say 'I don't have that information.'" Require citations. Lower temperature.
