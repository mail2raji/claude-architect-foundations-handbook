"""
Phase 3.5 - Ground-truth evaluation framework.

We compare 4 prompt versions on a 10-ticket dataset, print the accuracy
matrix. This is the core skill for the eval section of the exam.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# (ticket, expected_category)
DATASET = [
    ("Quarterly financial reporting macro is broken", "SOX"),
    ("Patient X-ray emailed to wrong physician", "HIPAA"),
    ("EU customer requested deletion of all data", "GDPR"),
    ("Tracking cookies dropped without consent in EU", "GDPR"),
    ("Coffee machine leaking", "Other"),
    ("DB admin can change financial tables w/o approval", "SOX"),
    ("Lost laptop with patient records, no encryption", "HIPAA"),
    ("German user got marketing email after opting out", "GDPR"),
    ("Printer jammed on 3rd floor", "Other"),
    ("CFO wants segregation of duties review for SAP", "SOX"),
]

PROMPTS = {
    "v1_naive":     "Classify this ticket as SOX, GDPR, HIPAA, or Other. Reply one word.\n{t}",
    "v2_xml":       "<task>Classify into SOX/GDPR/HIPAA/Other. One word only.</task>\n<ticket>{t}</ticket>",
    "v3_xml+rules": (
        "<task>Classify into SOX/GDPR/HIPAA/Other. One word only.</task>"
        "<rules>SOX=financial-reporting integrity. HIPAA=health PHI. "
        "GDPR=EU personal data. Other=everything else.</rules>"
        "<ticket>{t}</ticket>"
    ),
    "v4_xml+rules+cot": (
        "<task>Classify into SOX/GDPR/HIPAA/Other.</task>"
        "<rules>SOX=financial integrity. HIPAA=health PHI. "
        "GDPR=EU personal data.</rules>"
        "<ticket>{t}</ticket>"
        "Think in <thinking>. Then output ONLY the category word in <answer>."
    ),
}


def predict(prompt_template, ticket):
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300 if "<thinking>" in prompt_template else 10,
        temperature=0,
        messages=[{"role": "user", "content": prompt_template.format(t=ticket)}],
    ).content[0].text

    # extract <answer> if present, else use whole reply
    if "<answer>" in resp:
        import re
        m = re.search(r"<answer>(.*?)</answer>", resp, re.S)
        if m:
            resp = m.group(1)
    return resp.strip().strip(".").split()[0]   # first word, no trailing dot


results = {}
for name, tmpl in PROMPTS.items():
    correct = 0
    for ticket, expected in DATASET:
        pred = predict(tmpl, ticket)
        ok = pred.upper() == expected.upper()
        correct += ok
        print(f"  {name:18s} | {expected:5s} -> {pred:6s} {'✓' if ok else '✗'} | {ticket[:55]}")
    acc = correct / len(DATASET)
    results[name] = acc
    print(f"  ---- {name} accuracy: {acc:.0%} ----\n")

print("=== Summary ===")
for name, acc in results.items():
    print(f"  {name:18s} {acc:.0%}")
