# Domain 5 — Context Management & Reliability (RAG)

*Was Phase 5.* **Cert weight: 15%.**

**Maps to:** Skilljar "Retrieval augmented generation" (10 lessons). **Exam weight: ~12%.**
**Goal:** Give Claude domain knowledge it wasn't trained on — accurately and cheaply.

---

## 5.1 Why RAG?

Claude has two big limitations for company-specific Q&A:
1. **It doesn't know your internal docs.** They aren't in the training set.
2. **Context windows aren't free.** Even with 200K tokens you can't dump every PDF every call — costs add up.

RAG (Retrieval-Augmented Generation) fixes both:

```
Question ──► Retriever ──► top-k chunks ──► Claude ──► Grounded answer
                ▲
                │
        Vector DB / BM25 index built from your docs
```

You retrieve only the **few most relevant chunks** and put them into the prompt. Claude answers using just those chunks → cheaper, more accurate, citable.

---

## 5.2 The RAG pipeline — five stages

| Stage | Job | Tooling |
|---|---|---|
| **1. Chunking** | Split each document into pieces small enough to embed (~200–800 tokens). | Plain Python (recursive char splitter, sentence-aware) |
| **2. Embeddings** | Turn each chunk into a vector. | Voyage AI (`voyage-3-large`, partner of Anthropic) or others |
| **3. Indexing** | Store vectors + the source text. | FAISS / Pinecone / Chroma / pgvector. For this course: in-memory NumPy. |
| **4. Retrieval** | Convert question to vector, find nearest k chunks. Optionally combine with **BM25** (keyword) for **hybrid search**. | NumPy / `rank_bm25` |
| **5. Generation** | Send chunks + question to Claude with strict "answer only from context" rules. | `client.messages.create(...)` |

You'll build all five in `01_chunking.py` → `04_reranking.py`.

---

## 5.3 Critical concepts the exam tests

### Chunking strategies
- **Fixed-size**: simplest, every chunk N chars.
- **Recursive**: split on `\n\n`, then `\n`, then `.`, then chars. Preserves structure.
- **Semantic**: cluster sentences by embedding similarity. Slower, often best.

### Embeddings
A function `text -> vector ∈ ℝ^d`. Similar meaning → close vectors (cosine similarity). Same model must be used for both *documents* and *queries*.

### Hybrid search (vector + BM25)
- Vector search excels at **semantic** matches ("password help" finds "MFA reset").
- BM25 excels at **exact terms** (product names, error codes).
- Hybrid = run both, normalize scores, combine (e.g., Reciprocal Rank Fusion).

### Reranking
After getting top-25 with cheap retrievers, run a **cross-encoder reranker** (e.g., Voyage rerank, Cohere rerank) on those 25 to score (query, chunk) directly. Keep top-5 to send to Claude. Massive quality gain.

### Contextual retrieval (Anthropic's signature trick)
Before embedding/BM25-indexing a chunk, **prefix the chunk with a 1-paragraph Claude-generated summary of where it sits in the larger document**. That summary contains crucial context ("This chunk is part of the Q3 financial report, ARR section, …") that would otherwise be lost. Result: ~50% reduction in retrieval failure rate. Use **prompt caching** to keep this cheap.

---

## 5.4 Anti-patterns (exam favorites)

| Anti-pattern | Why it's bad | Fix |
|---|---|---|
| Putting the whole 200K doc in every call | Cost explodes | Retrieve chunks |
| Same chunk size for all doc types | One size fits none | Tune per source |
| Pure vector OR pure keyword | Misses 30% of intent | Hybrid |
| No reranking | Top-1 is often wrong | Add reranker |
| Letting Claude answer without `<context>` | It hallucinates | "Answer ONLY from the <context> block. If not present, say 'I don't know'." |
| Citing nothing | User can't verify | Ask for citations: `<answer>...</answer><sources>[chunk_id,…]</sources>` |

---

## 5.5 Real-world scenario

> **Internal IT KB chatbot.** 300 markdown KB articles. Employees ask "how do I reset MFA on a lost phone?" The bot must:
> - Retrieve relevant articles (hybrid)
> - Rerank
> - Answer with citations
> - Refuse if no good match
>
> You build a toy version of exactly this in `mini_project_kb_qa.py`.

---

## 5.6 Hands-on examples

| # | File | Topic |
|---|---|---|
| 1 | [`01_chunking.py`](01_chunking.py) | Recursive chunker over markdown |
| 2 | [`02_embeddings_and_search.py`](02_embeddings_and_search.py) | Voyage embeddings + cosine similarity (NumPy) |
| 3 | [`03_hybrid_bm25.py`](03_hybrid_bm25.py) | BM25 + vector + RRF fusion |
| 4 | [`04_reranking.py`](04_reranking.py) | Voyage rerank for top-k refinement |
| 5 | [`05_contextual_retrieval.py`](05_contextual_retrieval.py) | Claude-generated chunk context |
| 6 | [`mini_project_kb_qa.py`](mini_project_kb_qa.py) | Full pipeline with citations |

> Phases 5 requires `VOYAGE_API_KEY` for embedding/rerank. Free trial gives plenty for this course. Sign up at https://voyageai.com.

---

## 5.7 Exercises & mini quiz → [`exercises.md`](exercises.md)

Next → drill the exam-prep material per domain. Start with the heaviest: [Domain1_AgentArchitecture_27pct/exam_prep/](../Domain1_AgentArchitecture_27pct/exam_prep/).
