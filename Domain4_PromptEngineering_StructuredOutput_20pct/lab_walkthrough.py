"""
Domain 4 — Prompt Engineering & Structured Output (20% of the cert)
====================================================================
A SINGLE step-by-step walkthrough covering both Domain 4 halves:
  - API basics            (sub-folder api_basics/)
  - Prompt engineering    (sub-folder prompt_engineering/)

Run with:
    python Domain4_PromptEngineering_StructuredOutput_20pct/lab_walkthrough.py

STEPS:
    STEP 1 — First call: model, system, max_tokens, stop_reason (api basics).
    STEP 2 — Explicit-criteria prompt for code review (Lab 4.1).
    STEP 3 — Few-shot to fix ambiguous tool selection (Lab 4.2).
    STEP 4 — Structured output via tool_use as formatter (Lab 4.3).
    STEP 5 — Retry-with-feedback loop on schema failure (Lab 4.4).
    STEP 6 — Self-correction prompt for arithmetic (Lab 4.5).
    STEP 7 — Multi-instance and multi-pass review (Labs 4.6 / 4.7).
    STEP 8 — Batch API for non-blocking workloads (Lab 4.8).
    STEP 9 — Mini eval harness (Lab 4.9).

NETWORK: Steps 1, 2, 4, 6 make real API calls (cheap Haiku). Set
        ANTHROPIC_API_KEY OR comment those `client.messages.create` blocks.
"""

from __future__ import annotations
import os
import json
from dotenv import load_dotenv

load_dotenv()

try:
    from anthropic import Anthropic
    client = Anthropic()
    HAVE_API = bool(os.getenv("ANTHROPIC_API_KEY"))
except Exception:
    HAVE_API = False
    client = None


def banner(step: int, title: str) -> None:
    print(f"\n{'=' * 70}\n=== STEP {step}: {title}\n{'=' * 70}")


# ---------------------------------------------------------------------------
# STEP 1 — First call (API basics, was Phase 1/2)
# ---------------------------------------------------------------------------
banner(1, "First call: required fields + stop_reason")

print("""
The minimum viable call:
  client.messages.create(
      model='claude-haiku-4-5',
      max_tokens=200,           # REQUIRED — caps the response
      system='You are concise.',
      messages=[{'role': 'user', 'content': '...'}],
  )

The response carries a `stop_reason`:
  end_turn       -> natural stop
  max_tokens     -> hit the cap; consider raising
  tool_use       -> the model wants to call a tool
  stop_sequence  -> hit a user-supplied stop string
""")
if HAVE_API:
    r = client.messages.create(model="claude-haiku-4-5", max_tokens=60,
                               system="Reply in <=20 words.",
                               messages=[{"role": "user", "content": "Why is max_tokens required?"}])
    print(f"  stop_reason={r.stop_reason}  output={r.content[0].text!r}")


# ---------------------------------------------------------------------------
# STEP 2 — Explicit criteria for code review (Lab 4.1)
# ---------------------------------------------------------------------------
banner(2, "Explicit criteria beat 'review this code' (Lab 4.1)")

VAGUE = "Review this code."
EXPLICIT = """
Review the code below against THESE criteria, in this order:
  1. Correctness — would it crash, hang, or produce wrong output?
  2. Security — secrets in code, SQLi, eval(), path traversal?
  3. Tests — is the change covered? List missing cases.
  4. Style — only flag deviations from PEP-8 line length.

For each finding output ONE line:
  [SEVERITY] file:line  Description.  Remediation: ...
Severity is one of: BLOCKER, MAJOR, MINOR.
If no findings, output exactly: 'No findings.'
"""
print(f"  VAGUE   : {VAGUE!r}\n  EXPLICIT: see above. Note the rubric + the OUTPUT contract.\n")
# TRY THIS: run BOTH prompts on the same diff and grade the reviews against
# a held-out 'gold' review list. Explicit always wins on consistency.


# ---------------------------------------------------------------------------
# STEP 3 — Few-shot to fix ambiguous tool selection (Lab 4.2)
# ---------------------------------------------------------------------------
banner(3, "Few-shot examples disambiguate tool selection (Lab 4.2)")
FEW_SHOT = """
Examples of when to call each tool:

  User: "Search our policies for refund SLA."
  -> call search_internal_kb(query='refund SLA')

  User: "What's the score of the Lakers game right now?"
  -> call search_web(query='Lakers score today')

  User: "Tell me a joke."
  -> call NEITHER. Just answer.
"""
print(FEW_SHOT)
print("RULE: 3 examples is the sweet spot. Cover the positive case AND the 'do not call' case.")


# ---------------------------------------------------------------------------
# STEP 4 — Structured output via tool_use formatter (Lab 4.3)
# ---------------------------------------------------------------------------
banner(4, "Strict JSON via tool_use (Lab 4.3)")

CLASSIFIER_TOOL = {
    "name": "classify_ticket",
    "description": "Emit the final ticket classification as structured JSON.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category":   {"type": "string", "enum": ["billing", "technical", "refund", "other"]},
            "priority":   {"type": "string", "enum": ["low", "medium", "high", "urgent"]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": ["category", "priority", "confidence"],
    },
}


def classify(ticket: str) -> dict:
    if not HAVE_API:
        print(f"  (skipped) would classify: {ticket!r}")
        return {}
    r = client.messages.create(
        model="claude-haiku-4-5", max_tokens=300,
        tools=[CLASSIFIER_TOOL],
        tool_choice={"type": "tool", "name": "classify_ticket"},   # FORCE the schema
        messages=[{"role": "user", "content": ticket}],
    )
    for b in r.content:
        if getattr(b, "type", None) == "tool_use":
            return b.input
    return {}


print(classify("My invoice was double-charged, please refund $42."))
print("\nWHY THIS BEATS 'output JSON': enum validation is enforced by the API.")


# ---------------------------------------------------------------------------
# STEP 5 — Retry-with-feedback on schema failure (Lab 4.4)
# ---------------------------------------------------------------------------
banner(5, "Retry-with-feedback when schema parse fails (Lab 4.4)")

print("""
Pattern (no API call required to demo):
  1. Call -> parse JSON.
  2. If parse fails, build a NEW message:
       'Your last response was not valid JSON. Specific issue: <error>.
        Try again, and respond ONLY with valid JSON.'
  3. Append both the failed response AND the feedback to messages, then retry.
  4. Cap retries at 2. After that, escalate to a stronger model or human.
""")


def parse_or_retry_prompt(raw_text: str, parse_fn):
    try:
        return parse_fn(raw_text), None
    except Exception as e:
        feedback = (
            "Your previous response could not be parsed.\n"
            f"Parser error: {e}\n"
            "Please retry. Respond with VALID JSON ONLY, no prose."
        )
        return None, feedback


parsed, feedback = parse_or_retry_prompt("not really json", json.loads)
print(f"  parsed={parsed!r}  feedback (next user msg)=\n{feedback}")


# ---------------------------------------------------------------------------
# STEP 6 — Self-correction for arithmetic (Lab 4.5)
# ---------------------------------------------------------------------------
banner(6, "Self-correction prompt pattern (Lab 4.5)")
SELF_CORRECT = """
Solve the problem. Then in a <verify> block, RE-DERIVE the answer using a
different method and check the two match. If they differ, output the corrected
answer in a <final> block.

Problem: {problem}
"""
print(SELF_CORRECT.format(problem="A train travels 132 km in 1h 50min. Average speed in km/h?"))
print("""
This pattern raises arithmetic accuracy ~10-25% on multi-step problems for a
small token premium. Pair with <thinking>/<answer> XML tags for clean parsing.
""")


# ---------------------------------------------------------------------------
# STEP 7 — Multi-instance + multi-pass review (Labs 4.6 / 4.7)
# ---------------------------------------------------------------------------
banner(7, "Multi-instance vs multi-pass review (Labs 4.6 / 4.7)")
print("""
MULTI-INSTANCE  (independent reviewers, then aggregate):
  - Spawn 3 Claude calls with the SAME prompt, different temperatures.
  - Aggregate: union of findings, then dedupe.
  - Use for: high-stakes review where false-negatives are expensive.

MULTI-PASS  (different pass per concern):
  - Pass 1: per-file correctness review.
  - Pass 2: integration review across changed files.
  - Pass 3: security-specific review.
  - Use for: large diffs where one big prompt would overflow context or
            mix concerns.

DO NOT combine both blindly — costs multiply.
""")


# ---------------------------------------------------------------------------
# STEP 8 — Batch API (Lab 4.8)
# ---------------------------------------------------------------------------
banner(8, "Batch API for non-blocking jobs (Lab 4.8)")
print("""
WHEN to use Batch:
  - >1000 calls AND latency doesn't matter (offline scoring, nightly reports,
    eval harness runs).
  - You get ~50% discount vs interactive Messages API.

API SHAPE (sketch):
  request = client.messages.batches.create(
      requests=[
          {'custom_id': '1', 'params': {'model': ..., 'messages': [...]}},
          {'custom_id': '2', 'params': {'model': ..., 'messages': [...]}},
          ...
      ]
  )
  # Poll status; when 'ended', download the JSONL results.

DO NOT use Batch for: chat UIs, anything user-blocking, or <100 calls
(setup overhead dominates).
""")


# ---------------------------------------------------------------------------
# STEP 9 — Mini eval harness (Lab 4.9)
# ---------------------------------------------------------------------------
banner(9, "Eval harness — the only way to know a prompt change helped (Lab 4.9)")
EVAL_DATA = [
    {"input": "My invoice was double-charged", "expected": "refund"},
    {"input": "I cannot log into my account",   "expected": "technical"},
    {"input": "How do I add a credit card?",    "expected": "billing"},
]


def evaluate(predict_fn) -> float:
    correct = sum(predict_fn(c["input"]) == c["expected"] for c in EVAL_DATA)
    return correct / len(EVAL_DATA)


def naive_predict(text: str) -> str:
    t = text.lower()
    if "refund" in t or "double-charged" in t: return "refund"
    if "log" in t or "login" in t:             return "technical"
    return "billing"


print(f"  Naive baseline accuracy: {evaluate(naive_predict):.0%}")
print("""
PROMOTION RULE: a new prompt only ships if:
  (a) accuracy did NOT drop more than 1 pp, AND
  (b) cost did NOT increase more than 10%, AND
  (c) latency p95 did NOT increase more than 20%.
Always run the harness BEFORE merging a prompt change.
""")


# ---------------------------------------------------------------------------
# SELF-CHECK
# ---------------------------------------------------------------------------
print(f"\n{'=' * 70}\n=== SELF-CHECK\n{'=' * 70}")
print("""
  1. Name the 4 stop_reason values and what each means.
  2. Why does tool_use as formatter beat 'respond with JSON' for strict schemas?
  3. What two ingredients does a retry-with-feedback turn append?
  4. When is multi-pass review better than one big prompt?
  5. Three criteria that gate promoting a prompt change?
  6. What discount does Batch API give and what's its trade-off?
  7. Why is few-shot's 'do NOT call' example important?

Tick the checklist boxes in:
  Domain4_.../api_basics/exam_prep/final_checklist.md
  Domain4_.../prompt_engineering/exam_prep/final_checklist.md
""")
