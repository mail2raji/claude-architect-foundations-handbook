"""
Phase 7.6 - Evaluator-optimizer loop.

Generator (Sonnet) writes a draft. Evaluator (Opus) scores it 1-5 with
a rationale. If <5, the rationale is fed back. Repeat up to N rounds
or until score == 5.
"""

import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

TASK = (
    "Write a 3-sentence apology email to a customer whose flight was "
    "cancelled. Offer rebooking and a clear next step. Empathetic, not gushing."
)
RUBRIC = (
    "5 = empathetic, acknowledges issue, offers concrete next step, <=3 sentences\n"
    "4 = minor issues; 3 = wordy or vague; 2 = robotic; 1 = wrong or rude"
)

def gen(history):
    return client.messages.create(
        model="claude-sonnet-4-5", max_tokens=300, temperature=0.4,
        system="You write customer service emails.",
        messages=history,
    ).content[0].text.strip()

def judge(draft):
    prompt = (
        f"<task>{TASK}</task>\n<rubric>{RUBRIC}</rubric>\n<draft>{draft}</draft>\n"
        "Think in <thinking>, output integer 1-5 in <score>, and a single concrete "
        "improvement in <feedback>."
    )
    return client.messages.create(
        model="claude-opus-4-5", max_tokens=400, temperature=0,
        messages=[{"role": "user", "content": prompt}],
    ).content[0].text

history = [{"role": "user", "content": TASK}]
for round_ in range(3):
    draft = gen(history)
    print(f"\n--- Round {round_+1} draft ---\n{draft}")

    j = judge(draft)
    score = int(re.search(r"<score>\s*(\d)", j).group(1))
    feedback = re.search(r"<feedback>(.*?)</feedback>", j, re.S).group(1).strip()
    print(f"score={score} | feedback: {feedback}")

    if score == 5:
        print("\nDone.")
        break

    # feed feedback back so the generator improves
    history.append({"role": "assistant", "content": draft})
    history.append({"role": "user",
                    "content": f"Revise. Feedback: {feedback}"})
