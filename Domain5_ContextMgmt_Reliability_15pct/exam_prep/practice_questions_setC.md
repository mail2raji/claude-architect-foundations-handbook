# Practice Questions Set C (HARD, scenario-based) — Domain 5 — Context Management & Reliability (15%)

Sourced from the consolidated Set C (30 questions total). Each is a real-production scenario; many have plausible distractors.

Only the **3 questions tagged for this domain** appear here.

> Treat these as exam practice: read twice, eliminate clearly wrong answers, only then pick.

---

### 3. A RAG bot scores 92% on holdout questions but users complain it "makes things up" in production. The corpus is unchanged. Most likely root cause?
- A) Wrong embedding model
- B) System prompt doesn't constrain answers to retrieved context
- C) `temperature=0` is wrong; raise it
- D) Need more chunks

### 21. A retrieval system needs to find docs by exact rule name like "AC-2" AND by semantic similarity. Best retrieval?
- A) Pure vector
- B) Pure BM25
- C) Hybrid: vector + BM25 fused via RRF
- D) Pure rerank

### 22. The reranker improves end-to-end quality WHEN:
- A) The right doc is at rank 1 in vector search
- B) The right doc is in the top-N candidates but not at rank 1
- C) The right doc is NOT in the top-N candidates
- D) The corpus is small


---

## Answer key with explanations

| # | Ans | Source phase | Why |
|---|---|---|---|
| 3 | **B** | Phase 5 | If holdout passes but production fails, the system prompt isn't constraining the model to retrieved context. Add "Answer only from `<context>`; if missing say so." |
| 21 | **C** | Phase 5 | Hybrid is the production default. BM25 catches exact identifiers; vector catches semantics; RRF fuses them. |
| 22 | **B** | Phase 5 | A reranker can only re-order what retrieval returned. If the doc isn't in the top-N, reranking can't help — fix retrieval first. |
