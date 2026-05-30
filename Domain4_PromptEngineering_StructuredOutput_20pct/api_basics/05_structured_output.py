"""
Phase 2.5 - Structured output (JSON).

Two reliable patterns:

(A) PREFILLING - we put `{` as the start of the assistant turn so Claude
    MUST continue JSON. Cheap and quick. Works ~95% of the time.

(B) TOOL-USE-AS-FORMATTER - we define a tool whose input_schema is the
    JSON shape we want and force Claude to "call" it. The most RELIABLE
    technique. We cover the full version in Phase 4 - here is a teaser.

Real-world: a log-triage microservice that must return strict JSON.
"""

import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

LOG = (
    "2026-05-28 03:14:11 BLOCK src=10.0.4.22 dst=185.244.25.7 "
    "proto=TCP dport=4444 action=DENY rule=outbound-c2-block"
)

# -------- (A) PREFILLING --------
print("=== Pattern A: prefilling ===")
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    temperature=0,
    system=(
        "You output ONLY valid JSON matching schema "
        '{"severity":"low|medium|high|critical",'
        '"category":"network|auth|malware|other",'
        '"action":"<short imperative>"}'
    ),
    messages=[
        {"role": "user", "content": f"Triage this log:\n{LOG}"},
        {"role": "assistant", "content": "{"},   # prefill the JSON open brace
    ],
)
raw = "{" + resp.content[0].text          # don't forget to add back the prefix
data = json.loads(raw)
print(json.dumps(data, indent=2))


# -------- (B) TOOL-USE-AS-FORMATTER --------
print("\n=== Pattern B: tool-use-as-formatter ===")
tool = {
    "name": "record_triage",
    "description": "Record the triage decision for a single log line.",
    "input_schema": {
        "type": "object",
        "properties": {
            "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
            "category": {"type": "string", "enum": ["network", "auth", "malware", "other"]},
            "action":   {"type": "string"},
        },
        "required": ["severity", "category", "action"],
    },
}

resp2 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    temperature=0,
    tools=[tool],
    tool_choice={"type": "tool", "name": "record_triage"},   # force the tool
    messages=[{"role": "user", "content": f"Triage this log:\n{LOG}"}],
)

# Pull the tool_use block out
tool_use_block = next(b for b in resp2.content if b.type == "tool_use")
print(json.dumps(tool_use_block.input, indent=2))
