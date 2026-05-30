"""
Phase 7.2 - Prompt chain workflow with a quality gate.

Step 1: extract action items from a meeting transcript.
GATE  : if Step 1 returned no items, stop. Otherwise:
Step 2: rewrite each action item in SMART form.
Step 3: format as a Markdown checklist.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def ask(system, prompt, max_tokens=600):
    return client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=max_tokens,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    ).content[0].text.strip()


TRANSCRIPT = """
PM: Let's wrap up. Mark, can you finalize the RFP by Friday? Mark: yes.
Priya, please get HR sign-off on the new policy by end of next week.
And someone needs to schedule the architecture review - let's do that this month.
"""

# Step 1 - extract
items_raw = ask(
    "You extract action items.",
    f"<transcript>{TRANSCRIPT}</transcript>\n\n"
    "Extract action items. One per line: 'OWNER: ACTION'. If none, output 'NONE'.",
)
print("Step 1 raw:\n", items_raw, "\n")

# Gate
if items_raw.strip().upper().startswith("NONE"):
    print("No action items found - stopping early.")
    raise SystemExit

# Step 2 - SMART-ify
smart = ask(
    "You rewrite tasks in SMART form (Specific, Measurable, Assignable, Relevant, Time-bound).",
    f"<items>\n{items_raw}\n</items>\n"
    "Rewrite each as a single SMART sentence. One per line.",
)
print("Step 2 SMART:\n", smart, "\n")

# Step 3 - format
md = ask(
    "You format checklists in clean GitHub Markdown.",
    f"Convert this to a markdown checklist with owners bolded:\n{smart}",
)
print("Step 3 final:\n", md)
