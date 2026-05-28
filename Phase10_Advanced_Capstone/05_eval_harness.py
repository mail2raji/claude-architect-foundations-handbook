"""
CAPSTONE 5 — Enterprise Eval Harness
======================================

Scenario: You need to prove that swapping Sonnet -> Haiku in your classifier
won't regress quality. You also need a way to catch regressions when Anthropic
ships a new model version.

This is what real Anthropic-shop SREs build: a regression test suite for prompts.

Components:
  - Golden dataset (input + expected label / reference answer)
  - Run candidate models across the set
  - Two scoring modes:
      (a) exact / fuzzy match for classification
      (b) LLM-as-judge with rubric for open-ended
  - Per-model scoreboard + cost report
  - Regression detection vs baseline

Run:
  python 05_eval_harness.py
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

HAIKU = "claude-haiku-4-5"
SONNET = "claude-sonnet-4-5"
OPUS = "claude-opus-4-5"

# ----------------------- Golden dataset ----------------------- #

CLASSIFICATION_SET = [
    ("Reset my password", "account"),
    ("What time does the branch close?", "faq"),
    ("Lost my card and someone used it!", "complaint"),
    ("I want to dispute a 50 EUR charge", "account"),
    ("Your service is terrible, I'm leaving!", "complaint"),
    ("Is online banking down right now?", "faq"),
    ("Please freeze my debit card", "account"),
    ("Is there a branch in Berlin Mitte?", "faq"),
    ("My account got drained - call the regulator if you don't help", "complaint"),
    ("Can I set up direct deposit?", "faq"),
]

OPEN_ENDED_SET = [
    {
        "id": "OE-1",
        "prompt": "In <=80 words, explain why MFA reduces account takeover risk.",
        "rubric": "mentions: second factor, phished password alone insufficient, attacker needs device, brevity",
    },
    {
        "id": "OE-2",
        "prompt": "In <=80 words, describe GDPR's 72-hour breach notification rule.",
        "rubric": "mentions: GDPR Article 33, 72 hours, supervisory authority, awareness of breach, applies to controllers, brevity",
    },
]


# ----------------------- Helpers ----------------------- #

CLASSIFY_SYSTEM = """Classify the customer message into ONE category:
faq | account | complaint. Return ONLY the category word."""


@dataclass
class Result:
    model: str
    correct: int = 0
    total: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    failures: list[tuple[str, str, str]] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


def run_classifier(model: str) -> Result:
    r = Result(model=model)
    for msg, expected in CLASSIFICATION_SET:
        t0 = time.time()
        resp = client.messages.create(
            model=model,
            max_tokens=5,
            system=CLASSIFY_SYSTEM,
            messages=[{"role": "user", "content": msg}],
            temperature=0,
        )
        r.latency_ms += (time.time() - t0) * 1000
        r.input_tokens += resp.usage.input_tokens
        r.output_tokens += resp.usage.output_tokens
        pred = resp.content[0].text.strip().lower()
        r.total += 1
        if pred == expected:
            r.correct += 1
        else:
            r.failures.append((msg, expected, pred))
    return r


# ----------------------- Open-ended + LLM judge ----------------------- #

JUDGE_SYSTEM = """You grade a short answer against a rubric, on a 1-5 scale.
Return JSON: {"score": int, "reasons": "..."}.
- 5 = excellent, hits every rubric point with brevity
- 3 = adequate, some rubric points missing
- 1 = wrong or off-topic"""


def grade(answer: str, rubric: str) -> dict:
    resp = client.messages.create(
        model=OPUS,  # judge = strongest model
        max_tokens=200,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": f"<rubric>{rubric}</rubric>\n<answer>{answer}</answer>"}],
        temperature=0,
    )
    text = resp.content[0].text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"score": 0, "reasons": text[:120]}


def run_open_ended(model: str) -> list[dict]:
    out = []
    for case in OPEN_ENDED_SET:
        resp = client.messages.create(
            model=model,
            max_tokens=200,
            messages=[{"role": "user", "content": case["prompt"]}],
            temperature=0.3,
        )
        ans = resp.content[0].text
        g = grade(ans, case["rubric"])
        out.append({"id": case["id"], "model": model, "answer": ans, **g})
    return out


# ----------------------- Reporting ----------------------- #

def print_scoreboard(results: list[Result], open_ended: list[dict]):
    print("\n=== CLASSIFICATION SCOREBOARD ===")
    print(f"{'model':<22} {'acc':>6} {'in':>8} {'out':>8} {'lat_ms':>10}")
    for r in results:
        print(f"{r.model:<22} {r.accuracy:>5.0%} {r.input_tokens:>8} {r.output_tokens:>8} {r.latency_ms/r.total:>10.0f}")
    print("\n--- failures (baseline candidate) ---")
    for r in results:
        if r.failures:
            print(f"[{r.model}]")
            for msg, exp, got in r.failures:
                print(f"  expected={exp:<9} got={got:<9} :: {msg}")

    print("\n=== OPEN-ENDED LLM-JUDGE ===")
    by_model: dict[str, list[int]] = {}
    for row in open_ended:
        by_model.setdefault(row["model"], []).append(row["score"])
    for m, scores in by_model.items():
        avg = sum(scores) / len(scores)
        print(f"  {m:<22} avg={avg:.2f}  scores={scores}")

    # Regression check: is Haiku >= 90% of Sonnet accuracy?
    cls = {r.model: r.accuracy for r in results}
    if HAIKU in cls and SONNET in cls:
        ratio = cls[HAIKU] / cls[SONNET] if cls[SONNET] else 0
        print(f"\nRegression check: Haiku acc / Sonnet acc = {ratio:.2%} "
              f"({'PASS' if ratio >= 0.9 else 'FAIL'} 90% threshold)")


if __name__ == "__main__":
    results = [run_classifier(HAIKU), run_classifier(SONNET)]
    open_ended_results = run_open_ended(HAIKU) + run_open_ended(SONNET)
    print_scoreboard(results, open_ended_results)
