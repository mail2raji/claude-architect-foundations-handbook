# Glossary — Domain 5 — Context Management & Reliability (15%)

Subset of the cross-domain glossary, filtered to terms tagged for this domain.


## B
- **BM25** — Classic keyword retrieval algorithm. Use alongside vector search for hybrid retrieval. *(Phase 5)*

## C
- **Citation** — Asking the model to point to source `[id]` it used. Good RAG hygiene. *(Phase 5)*
- **Contextual retrieval** — Anthropic's recipe: prefix each chunk with a Claude-generated paragraph of context before indexing. *(Phase 5)*
- **Cross-encoder** — A model that takes (query, doc) together and scores relevance. Used in rerankers. *(Phase 5)*

## E
- **Embedding** — Vector representation of text. Same model for query and doc. *(Phase 5)*

## H
- **Hybrid search** — Combine vector + BM25 (often via RRF). *(Phase 5)*

## R
- **RAG (Retrieval-Augmented Generation)** — Fetch relevant chunks → put in prompt → answer from them. *(Phase 5)*
- **Reranking** — Cross-encoder scoring (q, doc) to refine top-k. *(Phase 5)*
- **RRF (Reciprocal Rank Fusion)** — Score = Σ 1/(k + rank). Combines multiple ranked lists. *(Phase 5)*
