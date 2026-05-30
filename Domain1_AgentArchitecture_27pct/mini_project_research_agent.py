"""
Phase 7 mini-project - Document research agent.

Composition of:
  ROUTER             (decides 'research' vs 'small-talk')
  ORCHESTRATOR       (plans sub-queries)
  PARALLEL WORKERS   (each does mini-RAG over a corpus)
  EVALUATOR-OPTIMIZER(final brief must cite >= 2 sources)

We keep the corpus tiny so it runs end-to-end in seconds.
"""

import concurrent.futures as cf
import json
import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

CORPUS = {
    "audit-2024": ("Vendor X: 3 critical findings related to MFA enforcement. "
                   "Remediation overdue by 60 days."),
    "audit-2025": ("Vendor X: improved on MFA but introduced new RBAC gaps. "
                   "Data-residency policy not signed."),
    "audit-2026": ("Vendor X: signed DPA. Pen-test passed. Three medium findings "
                   "open in API rate-limiting."),
    "support-tickets": ("Vendor X: 12 outages reported by EU customers in last 6 "
                        "months, average MTTR 4h."),
    "news": ("Vendor X acquired smaller competitor; integration risk for next FY."),
}


def call(model, sys, prompt, max_tokens=600, temp=0):
    return client.messages.create(
        model=model, max_tokens=max_tokens, temperature=temp, system=sys,
        messages=[{"role": "user", "content": prompt}],
    ).content[0].text


# ---- router --------------------------------------------------------------
def route(q):
    out = call("claude-haiku-4-5",
               "Classify as RESEARCH or SMALLTALK. One word.",
               q, max_tokens=10).strip().upper()
    return out


# ---- worker (mini-RAG over our corpus) -----------------------------------
def worker_answer(subq):
    # naive 'retrieval': keep all docs (corpus is tiny) and let Claude pick.
    ctx = "\n\n".join(f"[{k}] {v}" for k, v in CORPUS.items())
    return call("claude-sonnet-4-5",
                "Answer from <context> only. Cite sources like [src].",
                f"<context>\n{ctx}\n</context>\n<q>{subq}</q>",
                max_tokens=400)


# ---- evaluator-optimizer -------------------------------------------------
def evaluate(draft):
    j = call("claude-opus-4-5",
             "You are a strict editor.",
             f"<draft>{draft}</draft>\nDoes it cite >=2 distinct [source] tags AND "
             "directly answer the user request? Reply YES or NO and 1 line of feedback.",
             max_tokens=120)
    ok = "YES" in j.upper().split("\n")[0]
    return ok, j


# ---- main loop -----------------------------------------------------------
USER = "What's the risk profile of vendor X based on our recent audits and support data?"
print("Router:", route(USER))

# Plan
plan = json.loads(re.search(r"\[.*\]", call(
    "claude-opus-4-5",
    "You plan research. Output JSON list of subqueries.",
    f"Goal: {USER}\nList 3-5 subqueries as a JSON array of strings.",
    max_tokens=300,
), re.S).group(0))
print("Plan:", plan)

# Workers
with cf.ThreadPoolExecutor(max_workers=5) as ex:
    answers = list(ex.map(worker_answer, plan))

# Synthesize
joined = "\n\n".join(f"### {q}\n{a}" for q, a in zip(plan, answers))
for attempt in range(3):
    draft = call("claude-opus-4-5",
                 "You write executive risk briefings.",
                 f"<material>\n{joined}\n</material>\n"
                 f"Write a tight 200-word risk brief answering: {USER}\n"
                 "Cite sources inline as [src]. Include >=2 distinct sources.",
                 max_tokens=800)
    ok, why = evaluate(draft)
    print(f"\n--- attempt {attempt+1} ok={ok} ---\n{draft}\n[judge] {why}")
    if ok:
        break
