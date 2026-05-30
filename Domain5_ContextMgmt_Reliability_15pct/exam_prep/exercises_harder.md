# Harder Exercises — Domain 5 — Context Management & Reliability (15%)

Subset of the cross-domain 'harder exercises' file, filtered to this domain.
Each exercise expects an architect-level answer, not a tutorial-follower answer.

## (was Phase 5) RAG (harder)


**5H-1.** Construct a 200-doc corpus with 5 deliberately-similar docs. Show: pure-vector recall@5 vs hybrid recall@5 vs hybrid+rerank recall@5. Where is each architecture necessary?

**5H-2.** Implement contextual retrieval and measure embedding quality with vs without context, using a 50-question eval set. Cache the parent doc to keep cost down.

**5H-3.** Build a "refuse when not in context" guard and test it with 10 questions whose answer is NOT in the corpus. Your bot must say "I don't know" 10/10.

**5H-4.** Add semantic citation: every fact in the answer must point to a `[chunk_id]`. Penalize uncited claims.

**5H-5.** Build a query rewriter: transform the user's question into 3 query variants (decomposition + synonym + acronym expansion), retrieve for each, fuse with RRF. Measure recall lift.

---
