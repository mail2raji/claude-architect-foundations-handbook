"""
Domain 5 — Context Management & Reliability (15% of the cert)
==============================================================
A SINGLE step-by-step walkthrough that touches every Domain 5 sub-topic.

Run with:
    python Domain5_ContextMgmt_Reliability_15pct/lab_walkthrough.py

STEPS:
    STEP 1 — Extract a persistent 'case facts' block (Lab 5.1).
    STEP 2 — Trim verbose tool outputs (PostToolUse hook) (Lab 5.2).
    STEP 3 — Hybrid retrieval: vector + BM25 + rerank (RAG core).
    STEP 4 — Contextual retrieval: add a parent-doc preamble per chunk.
    STEP 5 — 'I don't know' guard: refuse when answer is NOT in context.
    STEP 6 — Cache the static prefix; observe input-token savings.
    STEP 7 — Observability: what to log on every call.

This file is NETWORK-FREE by default; every step is demonstrated with
in-memory data structures so you can re-read the patterns without burning
API tokens. Real implementations live in 02_rag_pipeline.py and the
capstones/02_compliance_rag_production.py file.
"""

from __future__ import annotations
import math
from collections import Counter


def banner(step: int, title: str) -> None:
    print(f"\n{'=' * 70}\n=== STEP {step}: {title}\n{'=' * 70}")


# ---------------------------------------------------------------------------
# STEP 1 — Persistent 'case facts' block (Lab 5.1)
# ---------------------------------------------------------------------------
banner(1, "Persistent 'case facts' block (Lab 5.1)")
print("""
PROBLEM: as a conversation grows, key facts (customer id, ticket id, account
balance) get buried in the transcript. The model occasionally 'forgets' them.

SOLUTION: maintain a CASE FACTS block at the top of every system prompt.
Update it deterministically as new facts arrive. NEVER let the LLM rewrite it.
""")


class CaseFacts:
    def __init__(self) -> None:
        self.facts: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self.facts[key] = value

    def render(self) -> str:
        if not self.facts:
            return ""
        lines = ["<case_facts>"]
        for k, v in self.facts.items():
            lines.append(f"  {k}: {v}")
        lines.append("</case_facts>")
        return "\n".join(lines)


cf = CaseFacts()
cf.set("customer_id", "C-9921")
cf.set("ticket_id", "T-44183")
cf.set("verified_email", "rita@example.com")
print(cf.render())
print("\nWhy <case_facts> tags? -> Claude respects XML tags and can be told to NEVER ignore them.")


# ---------------------------------------------------------------------------
# STEP 2 — Trim verbose tool outputs (Lab 5.2)
# ---------------------------------------------------------------------------
banner(2, "Trim verbose tool output before re-injecting (Lab 5.2)")
print("""
A tool that returns 5000 tokens of JSON poisons the context window AND
billable input tokens for every subsequent turn. Trim deterministically.
""")


def trim_tool_output(raw: dict, keep_keys: list[str], max_chars: int = 1500) -> dict:
    trimmed = {k: raw[k] for k in keep_keys if k in raw}
    rendered = str(trimmed)
    if len(rendered) > max_chars:
        rendered = rendered[:max_chars] + "...[truncated]"
        trimmed["_truncated"] = True
    return trimmed


SAMPLE = {"id": "A1", "name": "Acme", "address": "...", "history": ["e1"] * 200,
          "internal_notes": "x" * 4000, "balance": 12500}
print(f"  raw size  : {len(str(SAMPLE))} chars")
trimmed = trim_tool_output(SAMPLE, keep_keys=["id", "name", "balance"], max_chars=200)
print(f"  trimmed   : {trimmed}")
print("\nIn Claude Code, attach this via a PostToolUse hook so it runs on EVERY tool call.")


# ---------------------------------------------------------------------------
# STEP 3 — Hybrid retrieval (vector + BM25 + rerank)
# ---------------------------------------------------------------------------
banner(3, "Hybrid retrieval beats pure-vector RAG")
DOCS = [
    "Refunds for early CD withdrawal incur a 90-day-interest penalty.",
    "Section 4.2 of the member handbook defines the appeals process.",
    "Auto-loan payoff requests are processed within 5 business days.",
    "Online banking outages are reported on the status page.",
    "Fraud disputes must be filed within 60 days of the statement date.",
]


def bm25_like(query: str) -> list[tuple[int, float]]:
    q_tokens = query.lower().split()
    scores = []
    for i, d in enumerate(DOCS):
        d_tokens = d.lower().split()
        c = Counter(d_tokens)
        score = sum(c[t] for t in q_tokens)
        scores.append((i, float(score)))
    return sorted(scores, key=lambda x: -x[1])


def fake_vector_score(query: str) -> list[tuple[int, float]]:
    # Stand-in: 'semantic-ish' = overlap on stems
    stems = {"refund", "penalty", "section", "appeal", "loan", "outage", "fraud", "dispute"}
    q_stems = set(query.lower().split()) & stems
    scores = []
    for i, d in enumerate(DOCS):
        d_stems = set(d.lower().split()) & stems
        scores.append((i, len(q_stems & d_stems) / max(1, len(q_stems | d_stems))))
    return sorted(scores, key=lambda x: -x[1])


def reciprocal_rank_fusion(*ranked_lists, k=60) -> list[tuple[int, float]]:
    fused: dict[int, float] = {}
    for ranked in ranked_lists:
        for rank, (doc_id, _) in enumerate(ranked):
            fused[doc_id] = fused.get(doc_id, 0) + 1 / (k + rank)
    return sorted(fused.items(), key=lambda x: -x[1])


Q = "Section 4.2 early withdrawal refund penalty"
print(f"  query: {Q}")
print(f"  BM25 top-3:     {bm25_like(Q)[:3]}")
print(f"  Vector top-3:   {fake_vector_score(Q)[:3]}")
print(f"  Hybrid (RRF):   {reciprocal_rank_fusion(bm25_like(Q), fake_vector_score(Q))[:3]}")
print("""
WHY HYBRID: vector wins on semantic queries, BM25 wins on exact tokens
('Section 4.2'); fusion wins on the mix you actually see in production.
""")


# ---------------------------------------------------------------------------
# STEP 4 — Contextual retrieval
# ---------------------------------------------------------------------------
banner(4, "Contextual retrieval: prepend a per-chunk 'where am I' preamble")
RAW_CHUNK = "The penalty is 90 days of interest."
WITH_CONTEXT = (
    "From the Member Handbook -> Section 4.2 -> Early CD Withdrawal:\n"
    "The penalty is 90 days of interest."
)
print(f"  raw chunk        : {RAW_CHUNK!r}")
print(f"  contextual chunk : {WITH_CONTEXT!r}")
print("""
Anthropic's contextual-retrieval technique pre-computes a 1-sentence context
preamble per chunk using Haiku. It cuts retrieval failure ~35-50% with a small
one-time cost. Cache the parent doc to keep that cost flat.
""")


# ---------------------------------------------------------------------------
# STEP 5 — 'I don't know' guard
# ---------------------------------------------------------------------------
banner(5, "'I don't know' guard — refuse when the answer isn't in the chunks")
SYSTEM_GUARD = """
Answer ONLY from the chunks inside <context>. Each fact you state MUST be
followed by [chunk_id] citation. If the answer is NOT in the context, respond
with exactly: 'I don't have that information.' Do NOT speculate.
"""
print(SYSTEM_GUARD)
print("""
EVAL THIS: feed the bot 10 questions whose answer is NOT in the corpus.
A correctly-guarded bot says 'I don't have that information' 10/10.
A bot without the guard hallucinates 4-7/10. This is the most cost-effective
hallucination reducer in production RAG.
""")


# ---------------------------------------------------------------------------
# STEP 6 — Prompt caching
# ---------------------------------------------------------------------------
banner(6, "Cache the static prefix (~90% input-token savings)")
print("""
LAYOUT RULE: put CACHEABLE content at the TOP, VARIABLE content at the bottom.

    system = [
        {'type': 'text', 'text': BIG_STATIC_SYSTEM_PROMPT,
         'cache_control': {'type': 'ephemeral'}},
        {'type': 'text', 'text': PER_REQUEST_CASE_FACTS},
    ]

EFFECT:
  - First call: full input-token bill.
  - Subsequent calls within ~5 min: prefix bills at ~10% normal rate.
  - Renew the cache by sending similar traffic regularly.

DO NOT cache things that change per user (PII, case facts) -- defeats the
prefix match.
""")


# ---------------------------------------------------------------------------
# STEP 7 — Observability
# ---------------------------------------------------------------------------
banner(7, "What to log on EVERY call (so you can debug regressions)")
OBSERVABILITY_FIELDS = [
    "model_id (with snapshot)", "route_name", "parent_agent_id", "step_number",
    "input_tokens_cached", "input_tokens_uncached", "output_tokens",
    "latency_ms", "stop_reason",
    "tools_called (name, args_hash, success, latency_ms)",
    "retrieval_ids + ranks", "user_session (non-PII)",
    "error_class (if any)", "trace_id (for correlation across steps)",
]
for f in OBSERVABILITY_FIELDS:
    print(f"  - {f}")
print("""
Without these you CANNOT debug a regression. The bill spiked? Latency spiked?
Quality dropped? Each question is answerable only if these fields are logged.

ALERTING THRESHOLDS to start with:
  - accuracy drop >2 pp on the eval suite
  - input-token p95 change >25%
  - latency p95 change >30%
  - stop_reason mix shift (max_tokens up means truncation up)
""")


# ---------------------------------------------------------------------------
# SELF-CHECK
# ---------------------------------------------------------------------------
print(f"\n{'=' * 70}\n=== SELF-CHECK\n{'=' * 70}")
print("""
  1. Why is a 'case facts' block more reliable than letting the LLM remember?
  2. Why must tool outputs be trimmed BEFORE re-injecting?
  3. What does hybrid retrieval (vector + BM25 + rerank) buy you?
  4. What does contextual retrieval add per chunk, and at what cost?
  5. What single sentence in the system prompt halves hallucinations?
  6. Where does cacheable content go in the prompt and why?
  7. List 5 fields you must log on EVERY LLM call.

Tick the checklist in:
  Domain5_ContextMgmt_Reliability_15pct/exam_prep/final_checklist.md
""")
