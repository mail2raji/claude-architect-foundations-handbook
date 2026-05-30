"""
Phase 3.6 - LLM-as-judge for open-ended outputs.

Real-world: a customer support draft-reply assistant. There is no single
'correct' reply. We grade the reply on a 1-5 rubric using Claude Opus
(the judge) against expected facts.
"""

import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

QUESTION = "How do I reset my password if I no longer have access to my old phone for MFA?"

# What facts a good reply MUST cover.
EXPECTED_FACTS = [
    "Contact the helpdesk / IT support",
    "Identity verification will be required",
    "MFA factor will be re-enrolled",
    "Empathetic, professional tone",
]

# 1) get candidate reply from a cheaper model
candidate = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=400,
    system="You are a friendly IT helpdesk agent.",
    messages=[{"role": "user", "content": QUESTION}],
).content[0].text

print("--- candidate reply ---")
print(candidate)

# 2) judge it with Opus
JUDGE_PROMPT = f"""You are a strict grader.

<rubric>
5 = covers every expected fact AND has correct empathetic tone
4 = covers most facts, minor issues
3 = covers some facts, missing important ones
2 = misleading or rude
1 = wrong / hallucinated / harmful
</rubric>

<question>{QUESTION}</question>

<expected_facts>
{chr(10).join('- ' + f for f in EXPECTED_FACTS)}
</expected_facts>

<candidate_answer>
{candidate}
</candidate_answer>

Think in <thinking> tags, then output ONLY the integer 1-5 in <score> tags."""

judge_resp = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=500,
    temperature=0,
    messages=[{"role": "user", "content": JUDGE_PROMPT}],
).content[0].text

print("\n--- judge raw ---")
print(judge_resp)

m = re.search(r"<score>\s*(\d)\s*</score>", judge_resp)
print("\nFinal score:", m.group(1) if m else "?")
