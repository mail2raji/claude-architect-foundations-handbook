"""
Domain 1 — Agent Architecture & Orchestration (27% of the cert)
================================================================
A SINGLE step-by-step lab walkthrough that touches every Domain 1 sub-topic.

Run with:
    python Domain1_AgentArchitecture_27pct/lab_walkthrough.py

What you will do (each STEP prints a banner before it runs):
    STEP 1 — Drive the agent loop off `stop_reason` (Lab 1.1).
    STEP 2 — Pick the right workflow pattern for 4 scenarios (Lab 1.2).
    STEP 3 — Build a tiny ReAct agent with all 3 safety knobs (Lab 1.3).
    STEP 4 — Add a deterministic "hook" gate before a destructive tool (Lab 1.4).
    STEP 5 — Hub-and-spoke handoff with EXPLICIT context passing (Lab 1.5).
    STEP 6 — Task decomposition: parallel vs sequential subtasks (Lab 1.6).
    STEP 7 — Session control: when to resume, fork, or restart (Lab 1.7).

NETWORK: Steps 1, 3, 5 make real API calls (cheap Haiku). Set ANTHROPIC_API_KEY
        in your environment OR comment out the `client.messages.create` lines.

After running, scroll to the SELF-CHECK section at the end.
"""

from __future__ import annotations
import os
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
# STEP 1 — Drive the agent loop off `stop_reason`
# ---------------------------------------------------------------------------
banner(1, "Drive the loop off stop_reason (Lab 1.1)")
print("""
The ONE rule of an agent loop: keep iterating until stop_reason == 'end_turn'.
NEVER look for keywords like 'DONE' or 'final answer' in the text.
""")

WEATHER_TOOL = {
    "name": "get_weather",
    "description": "Get current weather for a city.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}


def fake_weather(city: str) -> str:
    return f"{city}: 22C, partly cloudy"


def run_loop_demo() -> None:
    if not HAVE_API:
        print("(skipped — no ANTHROPIC_API_KEY) — but here is the loop skeleton:")
        print(LOOP_SKELETON)
        return
    msgs = [{"role": "user", "content": "What is the weather in Sydney and Paris?"}]
    steps = 0
    while steps < 5:  # SAFETY KNOB #1: max_steps
        steps += 1
        resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=400,
            tools=[WEATHER_TOOL],
            messages=msgs,
        )
        print(f"  iter {steps}: stop_reason={resp.stop_reason}")
        msgs.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason == "end_turn":
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    print(f"  FINAL: {block.text[:200]}")
            break
        if resp.stop_reason == "tool_use":
            tool_results = []
            for block in resp.content:
                if getattr(block, "type", None) == "tool_use":
                    result = fake_weather(block.input.get("city", "?"))
                    tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            msgs.append({"role": "user", "content": tool_results})


LOOP_SKELETON = """
while steps < MAX_STEPS:
    resp = client.messages.create(model=..., tools=[...], messages=msgs)
    if resp.stop_reason == 'end_turn': break
    if resp.stop_reason == 'tool_use': msgs += execute(resp); continue
    if resp.stop_reason == 'max_tokens': retry_with_more_tokens(); continue
"""

run_loop_demo()
# TRY THIS: change MAX_STEPS to 1 and re-run. You'll see the loop end early
# before Claude can call BOTH tools — confirming why max_steps is a safety knob,
# not a debugging-only feature.


# ---------------------------------------------------------------------------
# STEP 2 — Pick the right pattern for each scenario (Lab 1.2)
# ---------------------------------------------------------------------------
banner(2, "Workflow pattern selection (Lab 1.2)")

SCENARIOS = [
    ("Same input, ask Claude 5x, take majority vote", "Parallelization (voting)"),
    ("Planner splits work, workers run in parallel, planner synthesizes", "Orchestrator-workers"),
    ("Classify ticket then route to billing/tech/refund specialist",   "Routing"),
    ("Draft -> critique -> revise -> critique -> stop when rubric passes", "Evaluator-optimizer"),
]
for scenario, expected in SCENARIOS:
    print(f"  Q: {scenario}")
    print(f"  A: {expected}\n")

print("RULE OF THUMB: prefer the SIMPLEST pattern. Workflows beat agents whenever both fit.")
# TRY THIS: cover the 'A' column with your finger and answer each one cold.


# ---------------------------------------------------------------------------
# STEP 3 — A ReAct agent with all 3 safety knobs (Lab 1.3)
# ---------------------------------------------------------------------------
banner(3, "ReAct agent with max_steps + token budget + tool allow-list (Lab 1.3)")

print("""
The three knobs every autonomous agent MUST have:
  1. max_steps           -> bounded loop iterations
  2. token budget        -> bounded API spend
  3. tool allow-list     -> bounded blast radius
""")


def react_agent(query: str, max_steps: int = 5, token_budget: int = 4000, allow_tools=None):
    if not HAVE_API:
        print(f"  (skipped) would run ReAct on: {query!r}")
        return
    allow_tools = allow_tools or [WEATHER_TOOL]
    tokens_used = 0
    msgs = [{"role": "user", "content": query}]
    for step in range(1, max_steps + 1):
        if tokens_used > token_budget:
            print(f"  STOPPED at step {step}: token budget {token_budget} exceeded.")
            return
        resp = client.messages.create(model="claude-haiku-4-5", max_tokens=300,
                                      tools=allow_tools, messages=msgs)
        tokens_used += resp.usage.input_tokens + resp.usage.output_tokens
        print(f"  step {step}: stop={resp.stop_reason}, total_tokens={tokens_used}")
        msgs.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason == "end_turn":
            return
        if resp.stop_reason == "tool_use":
            results = []
            for b in resp.content:
                if getattr(b, "type", None) == "tool_use":
                    if b.name not in {t["name"] for t in allow_tools}:
                        results.append({"type": "tool_result", "tool_use_id": b.id,
                                        "content": "ERROR: tool not allow-listed", "is_error": True})
                    else:
                        results.append({"type": "tool_result", "tool_use_id": b.id,
                                        "content": fake_weather(b.input.get("city", "?"))})
            msgs.append({"role": "user", "content": results})
    print(f"  STOPPED: max_steps={max_steps} reached.")


react_agent("Weather in Tokyo?")
# TRY THIS: call react_agent(...) with token_budget=50 to see the budget knob trigger.


# ---------------------------------------------------------------------------
# STEP 4 — Deterministic hook BEFORE a destructive tool (Lab 1.4)
# ---------------------------------------------------------------------------
banner(4, "Pre-tool hook gate (Lab 1.4)")
print("""
LLM 'please confirm' is not a control. A HOOK is a deterministic check that
runs BEFORE the tool call and can refuse it.
""")

DESTRUCTIVE = {"delete_customer", "transfer_funds", "drop_table"}


def pre_tool_hook(tool_name: str, args: dict, human_approval_token: str | None) -> tuple[bool, str]:
    if tool_name in DESTRUCTIVE and not human_approval_token:
        return False, f"BLOCKED: {tool_name} requires human approval token"
    if tool_name == "transfer_funds" and args.get("amount", 0) > 10_000:
        return False, "BLOCKED: amount exceeds $10K cap"
    return True, "OK"


for call in [
    ("get_weather", {"city": "Paris"}, None),
    ("transfer_funds", {"amount": 50_000}, "approval_abc"),
    ("delete_customer", {"id": "C42"}, None),
]:
    ok, reason = pre_tool_hook(*call)
    print(f"  {call[0]:18}  -> {'ALLOW' if ok else 'DENY '}  ({reason})")
# TRY THIS: add an audit log entry on every DENY so you can investigate later.


# ---------------------------------------------------------------------------
# STEP 5 — Hub-and-spoke with EXPLICIT context passing (Lab 1.5)
# ---------------------------------------------------------------------------
banner(5, "Hub-and-spoke handoff (Lab 1.5)")
print("""
Sub-agents do NOT share memory. The orchestrator must explicitly pass:
  - the task summary
  - any facts already gathered
  - the EXPECTED output shape
Otherwise the worker re-derives everything from scratch and burns tokens.
""")


def orchestrator(ticket: str) -> dict:
    if not HAVE_API:
        return {"classification": "(skipped — no API)"}
    # Hub call: classify
    sys = "Output ONE word: billing | technical | refund."
    classification = client.messages.create(model="claude-haiku-4-5", max_tokens=10,
                                            system=sys, messages=[{"role": "user", "content": ticket}]
                                            ).content[0].text.strip().lower()
    print(f"  hub classified -> {classification}")
    # Spoke call: handle, with EXPLICIT context handoff
    spoke_sys = (
        f"You are the {classification} specialist. "
        f"Context already established by the orchestrator: classification={classification}. "
        "Respond in <=30 words."
    )
    spoke_resp = client.messages.create(model="claude-haiku-4-5", max_tokens=120,
                                        system=spoke_sys, messages=[{"role": "user", "content": ticket}]
                                        ).content[0].text.strip()
    return {"classification": classification, "response": spoke_resp}


print(orchestrator("My invoice for $200 looks wrong, please refund the duplicate charge."))
# TRY THIS: drop the spoke_sys context and observe duplicate classification work.


# ---------------------------------------------------------------------------
# STEP 6 — Task decomposition strategies (Lab 1.6)
# ---------------------------------------------------------------------------
banner(6, "Decompose: parallel vs sequential (Lab 1.6)")
print("""
Two questions before you decompose:
  (a) Are subtasks INDEPENDENT?  -> parallel (sectioning)
  (b) Does subtask N need output of subtask N-1?  -> sequential (chain)
Picking parallel when subtasks are dependent corrupts the final answer.
""")

TASKS = [
    ("Translate one document into 5 languages", "PARALLEL (sectioning) — each language independent"),
    ("Extract action items -> rewrite SMART -> format checklist", "SEQUENTIAL (chain) — each step needs the previous"),
    ("Ask 5 reviewers for an independent code-review pass", "PARALLEL (voting) — aggregate at the end"),
    ("Search docs -> read top hit -> summarize", "SEQUENTIAL (chain) — read depends on search"),
]
for t, a in TASKS:
    print(f"  {t}\n    -> {a}\n")


# ---------------------------------------------------------------------------
# STEP 7 — Sessions: resume vs fork vs restart (Lab 1.7)
# ---------------------------------------------------------------------------
banner(7, "Session control (Lab 1.7)")
print("""
  RESUME  — continue the same conversation tomorrow with FULL history.
  FORK    — branch a working session to try an experimental change without
            polluting the main thread.
  RESTART — context is poisoned (bad facts cached, prompt-injection landed,
            or you're switching task). Start clean. Carry forward only the
            verified facts you copy yourself.
""")
SCENARIO_TO_OP = [
    ("User returns 2 days later to keep debugging the SAME bug", "RESUME"),
    ("You want to try a riskier refactor without losing the safe state", "FORK"),
    ("Agent absorbed prompt-injection text from a tool result", "RESTART"),
    ("Switching from 'write tests' to 'design new feature'", "RESTART"),
]
for s, op in SCENARIO_TO_OP:
    print(f"  {s}\n    -> {op}\n")


# ---------------------------------------------------------------------------
# SELF-CHECK
# ---------------------------------------------------------------------------
print(f"\n{'=' * 70}\n=== SELF-CHECK (close the file and answer these from memory)\n{'=' * 70}")
print("""
  1. What is the ONE field that ends an agent loop?
  2. Name the 5 workflow patterns and one scenario each.
  3. List the 3 mandatory safety knobs on every autonomous agent.
  4. Why is an LLM 'please confirm' NOT a control? What replaces it?
  5. What two things MUST an orchestrator pass to a sub-agent?
  6. When does a task require sequential decomposition rather than parallel?
  7. When should you RESTART a session instead of resuming it?

When you can answer all 7 without notes, tick the Domain 1 checklist boxes in
  Domain1_AgentArchitecture_27pct/exam_prep/final_checklist.md
""")
