"""
Phase 7.4 - Parallel workflow.

(a) SECTIONING: split a 4-section report; each section drafted in parallel; merge.
(b) VOTING   : same classification asked 5 times; majority answer wins.
"""

import concurrent.futures as cf
from collections import Counter
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def msg(prompt, system="", model="claude-sonnet-4-5", temp=0, max_tokens=400):
    return client.messages.create(
        model=model, max_tokens=max_tokens, temperature=temp, system=system,
        messages=[{"role": "user", "content": prompt}],
    ).content[0].text


# ---- (a) sectioning -------------------------------------------------------
SECTIONS = ["Threats", "Vulnerabilities", "Controls", "Recommendations"]
TOPIC = "Public-facing web app handling EU PII"

def draft(section):
    return section, msg(
        f"Draft the '{section}' section (3 bullets) of a security review for: {TOPIC}",
        system="You are a senior security architect. Be concise.",
    )

print("=== SECTIONING ===")
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    parts = list(ex.map(draft, SECTIONS))
for name, body in parts:
    print(f"\n## {name}\n{body}")


# ---- (b) voting -----------------------------------------------------------
print("\n=== VOTING ===")
TICKET = "EU customer wants their account and data fully deleted"
PROMPT = f"Classify into SOX/GDPR/HIPAA/Other. Ticket: {TICKET}. One word only."

def one_vote(_):
    return msg(PROMPT, temp=0.7, max_tokens=10).strip().upper()

with cf.ThreadPoolExecutor(max_workers=5) as ex:
    votes = list(ex.map(one_vote, range(5)))
print("votes:", votes)
print("winner:", Counter(votes).most_common(1)[0][0])
