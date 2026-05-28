# Production Cost & Latency Cheat-Sheet

Order-of-magnitude rules for production Claude systems.

## Pricing intuition (approximate)

| Tier | Input $/M tok | Output $/M tok | Latency | Use it for |
|---|---|---|---|---|
| Haiku 4.x | very low | very low | fastest | classification, extraction, routing, formatters |
| Sonnet 4.x | medium | medium | medium | default app workhorse, tool use, RAG answer |
| Opus 4.x | high | high | slowest | planning, judging, hardest analysis |

> Exact numbers change. The **ratio** (Haiku ≪ Sonnet ≪ Opus, often >10× between tiers) is what matters for architecture.

## Output is the silent killer

Output tokens typically cost **5× input** tokens on the same tier. If a system feels expensive, the first thing to inspect is **output length**, not prompt size.

Levers:
- "Reply in JSON only. No explanations." (saves 80% on output).
- `max_tokens` set to the realistic ceiling, not the maximum.
- Prefill `{` to skip a preamble.

## Caching ROI

Prompt caching pays back on the **2nd to N-th** call within the 5-min window.

| Pattern | Worth caching? |
|---|---|
| 50K system prompt reused 100×/hour | YES (huge win) |
| 50K system prompt called once | NO (you pay the write cost) |
| RAG context that changes per query | NO |
| RAG **system rules + tool defs** that are static | YES |
| Few-shot examples that never change | YES |

Rule: cache the static prefix; don't cache anything that varies.

## RAG cost shape

Per query (typical production):
- 1 embed of the query (cheap)
- Vector search (cheap, your infra)
- Rerank top-25 → top-5 (small Claude call OR rerank-2 model)
- Final Claude call with top-5 chunks (~3K tokens input + answer)

Most cost comes from the **final answer call**, not embeddings.

## Latency budget

| Step | Typical ms |
|---|---|
| Embedding | 50–200 |
| Vector search | 20–100 |
| Reranker | 100–400 |
| Claude Haiku response | 300–800 |
| Claude Sonnet response | 700–2500 |
| Claude Opus response | 1500–6000 |
| Streamed first token | 200–800 |

For chat UX, **stream**. Total wall-clock cost doesn't change but perceived latency drops sharply.

## Scaling levers in priority order

1. **Right-size the tier.** Don't pay Opus prices for Haiku work.
2. **Cache static prefixes.**
3. **Shrink output.** JSON-only, short rubrics.
4. **Parallelize independent calls** (sectioning).
5. **Batch API** for any non-realtime workload.
6. **Pre-filter with a cheap classifier** to skip expensive calls entirely.
7. **Cache retrieval results** (your infra) for repeated queries.

## When to escalate Haiku → Sonnet → Opus

Heuristic: build a small eval set of 50–100 cases. Run Haiku. If score < your bar, try Sonnet on the failures. Only escalate the *failures*, not all traffic, to higher tiers (router pattern).

This is the same pattern as "fast path + slow path" in distributed systems.

## Observability checklist

A production Claude system should log per call:
- Model id
- Input tokens (prompt + cached read/write split)
- Output tokens
- Latency
- `stop_reason`
- Tool calls (name, args hash, result success)
- Retrieval hits (doc ids, ranks)
- User session id (for analytics, not PII)

Without these you cannot answer "why did our bill double?" or "why did quality drop?"
