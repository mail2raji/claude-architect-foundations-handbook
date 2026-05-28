"""
Phase 7.3 - Router workflow.

A cheap Haiku classifies the incoming question into one of three tiers:
  SIMPLE  -> Haiku  (fast/cheap)
  MEDIUM  -> Sonnet
  HARD    -> Opus   (deep reasoning)

This pattern saves significant cost in production.
"""

import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

ROUTER_PROMPT = """<task>
Classify the user's request by difficulty.
SIMPLE  = factual lookup, definitions, single-step
MEDIUM  = multi-step reasoning, writing, summarization
HARD    = math proofs, deep planning, multi-doc synthesis
</task>

<request>{q}</request>

Output ONLY one word: SIMPLE, MEDIUM, or HARD."""

TIER_TO_MODEL = {
    "SIMPLE": "claude-haiku-4-5",
    "MEDIUM": "claude-sonnet-4-5",
    "HARD":   "claude-opus-4-5",
}


def route(q: str) -> str:
    txt = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        temperature=0,
        messages=[{"role": "user", "content": ROUTER_PROMPT.format(q=q)}],
    ).content[0].text.strip().upper()
    return re.findall(r"SIMPLE|MEDIUM|HARD", txt + " MEDIUM")[0]   # safe fallback


def answer(q: str) -> str:
    tier = route(q)
    model = TIER_TO_MODEL[tier]
    print(f"[router] {tier} -> {model}")
    return client.messages.create(
        model=model, max_tokens=600, temperature=0,
        messages=[{"role": "user", "content": q}],
    ).content[0].text


if __name__ == "__main__":
    for q in [
        "What is the capital of France?",
        "Write a 200-word vendor risk paragraph for an internal audit report.",
        "Prove that there are infinitely many primes, step by step.",
    ]:
        print("\nQ:", q)
        print(answer(q)[:300], "...")
