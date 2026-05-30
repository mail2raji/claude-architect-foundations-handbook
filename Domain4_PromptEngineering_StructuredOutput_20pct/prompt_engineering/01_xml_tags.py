"""
Phase 3.1 - XML tags vs naive prompting.

Same task, two prompts. Compare outputs.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

TICKET = (
    "User in EU branch reports that our marketing site is dropping a tracking "
    "cookie without showing the consent banner. Legal CC'd."
)

NAIVE = f"Classify this ticket as SOX, GDPR, HIPAA, or Other:\n{TICKET}"

STRUCTURED = f"""<task>
Classify the support ticket into exactly one category: SOX, GDPR, HIPAA, or Other.
</task>

<rules>
- Output only the category word. Nothing else.
- If multiple apply, pick the most relevant.
</rules>

<ticket>
{TICKET}
</ticket>"""


def ask(prompt):
    return client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=20,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    ).content[0].text.strip()


print("Naive     :", ask(NAIVE))
print("Structured:", ask(STRUCTURED))
