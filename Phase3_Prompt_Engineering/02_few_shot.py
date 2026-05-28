"""
Phase 3.2 - Few-shot prompting.

We add 5 examples and re-classify the same ticket. Especially powerful
for edge-case wording the model would otherwise misread.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

EXAMPLES = [
    ("Quarterly financial reporting macro is broken in Excel", "SOX"),
    ("Patient X-ray accidentally emailed to wrong physician", "HIPAA"),
    ("EU customer asked to delete their account and all personal data", "GDPR"),
    ("Our marketing site dropped tracking cookies without consent banner in EU", "GDPR"),
    ("Coffee machine in break room is leaking", "Other"),
]

example_block = "\n".join(
    f"<example>\n<ticket>{t}</ticket>\n<category>{c}</category>\n</example>"
    for t, c in EXAMPLES
)

TICKET = (
    "Auditor flagged that our DB admin can change financial transaction "
    "tables without an approval workflow."
)

PROMPT = f"""<task>
Classify the support ticket into exactly one of: SOX, GDPR, HIPAA, Other.
Output only the category word.
</task>

<examples>
{example_block}
</examples>

<ticket>
{TICKET}
</ticket>"""

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20,
    temperature=0,
    messages=[{"role": "user", "content": PROMPT}],
)
print("Category:", resp.content[0].text.strip())
