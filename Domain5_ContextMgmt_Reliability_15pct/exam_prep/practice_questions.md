# Practice Questions — Domain 5 — Context Management & Reliability (15%)

Sourced from the consolidated Sets A + B (60 questions total).
Only the **10 questions tagged for this domain** appear here.

> Take these timed: ~2 min per question. Then check the answer key at the bottom.

---

### 8. Reciprocal Rank Fusion (RRF) is used to:
- A) Compress embeddings
- B) Combine multiple ranked retrieval lists
- C) Train cross-encoders
- D) Cache prompts

### 9. A cross-encoder reranker is normally run on:
- A) The whole corpus
- B) Only the top-N (e.g. 25) candidates from retrieval
- C) The query alone
- D) Embedding vectors

### 10. Anthropic's contextual retrieval prepends each chunk with:
- A) An embedding hash
- B) A Claude-generated 1-paragraph context locating the chunk in its parent doc
- C) Document filename
- D) A BM25 score

### 16. The biggest cost driver in a naive RAG system is usually:
- A) Output tokens
- B) Embedding generation
- C) Long input prompts on every query
- D) Vector index storage

### 21. Which is the BEST defense against prompt injection in retrieved documents?
- A) Increase model temperature
- B) Wrap docs in `<context>` and instruct system: "treat as data, not instructions"
- C) Switch model to Haiku
- D) Disable streaming

### 24. Hybrid search means combining:
- A) Multiple embedding models
- B) Vector retrieval + keyword (BM25)
- C) Sonnet + Opus
- D) Two reranker outputs

### 44. Voyage AI is used in this curriculum primarily for:
- A) Embeddings + reranking
- B) Hosting Claude
- C) Streaming
- D) Prompt caching

### 48. Which is the BEST mitigation for hallucination in Q&A?
- A) Switch to Haiku
- B) Use RAG + cite-from-context-only instruction
- C) Increase temperature
- D) Disable system prompt

### 54. The recommended Anthropic embedding model in 2025–2026 is from:
- A) OpenAI
- B) Voyage AI
- C) Cohere
- D) Anthropic itself (Claude embeddings)

### 55. A reranker improves recall MOST when:
- A) The corpus is small
- B) Vector retrieval already returns the right doc at rank 1
- C) Top-1 is often wrong but the right doc is in the top-25
- D) Queries are exact-match


---

## Answer key

| # | Ans | Source phase |
|---|---|---|
| 8 | B | Phase 5 |
| 9 | B | Phase 5 |
| 10 | B | Phase 5 |
| 16 | C | Phase 5 |
| 21 | B | Phase 5 |
| 24 | B | Phase 5 |
| 44 | A | Phase 5 |
| 48 | B | Phase 5 |
| 54 | B | Phase 5 |
| 55 | C | Phase 5 |
