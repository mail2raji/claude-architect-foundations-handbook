"""
Phase 7.5 - Orchestrator-workers.

The orchestrator (Opus) reads a user request and produces a PLAN: a list
of small subtasks. Each subtask is dispatched to a worker (Sonnet) in
parallel. The orchestrator then synthesizes the final answer.

Use case: "Write a competitive brief on cloud KMS offerings."
"""

import concurrent.futures as cf
import json
import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def call(model, system, prompt, max_tokens=900, temp=0):
    return client.messages.create(
        model=model, max_tokens=max_tokens, temperature=temp,
        system=system, messages=[{"role": "user", "content": prompt}],
    ).content[0].text


REQUEST = "Write a short competitive brief on Azure Key Vault vs AWS KMS vs GCP KMS."

# ---- 1) plan -------------------------------------------------------------
plan_raw = call(
    "claude-opus-4-5",
    "You are a planner. Output ONLY a JSON list of 4-6 worker subtasks, "
    'each like {"id":"w1","topic":"..."}.',
    f"Goal: {REQUEST}\nReturn JSON only.",
)
plan = json.loads(re.search(r"\[.*\]", plan_raw, re.S).group(0))
print("PLAN:")
for p in plan: print(" -", p)


# ---- 2) workers ----------------------------------------------------------
def worker(task):
    out = call(
        "claude-sonnet-4-5",
        "You are a research analyst. Write a tight 80-word paragraph.",
        f"Topic for the brief: {task['topic']}",
        max_tokens=300,
    )
    return task["id"], task["topic"], out

with cf.ThreadPoolExecutor(max_workers=6) as ex:
    drafts = list(ex.map(worker, plan))


# ---- 3) synthesize -------------------------------------------------------
joined = "\n\n".join(f"## {t}\n{b}" for _, t, b in drafts)
final = call(
    "claude-opus-4-5",
    "You are an editor. Merge sections into one cohesive 400-word brief. "
    "Add a 1-sentence executive summary at the top. Keep claims grounded.",
    f"<sections>\n{joined}\n</sections>",
    max_tokens=1200,
)
print("\n===== FINAL BRIEF =====\n")
print(final)
