"""
Phase 3.3 - Chain-of-thought (CoT).

We ask Claude to think in <thinking> tags first, then commit to an answer
in <answer> tags. We then parse out the answer.

Real-world: license-key math. Claude is bad at arithmetic without thinking,
much better with CoT.
"""

import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

QUESTION = (
    "We have 1,250 employees. 64% need an M365 E5 license at $57/user/mo. "
    "The rest get E3 at $36/user/mo. What's the yearly cost? Show working."
)

PROMPT = f"""<task>{QUESTION}</task>

First think step by step inside <thinking> tags.
Then put ONLY the final dollar amount inside <answer> tags."""

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=600,
    temperature=0,
    messages=[{"role": "user", "content": PROMPT}],
)
text = resp.content[0].text
print("--- raw ---\n", text, "\n")

m = re.search(r"<answer>(.*?)</answer>", text, re.S)
print("Extracted answer:", m.group(1).strip() if m else "NOT FOUND")
