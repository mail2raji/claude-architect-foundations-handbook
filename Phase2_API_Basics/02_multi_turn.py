"""
Phase 2.2 - Multi-turn conversation (memory by sending the whole history).

Real-world: a tiny on-call assistant CLI. Type your question, get a reply,
keep going. Type 'exit' to quit.

Key insight: Claude is STATELESS. YOU keep the history list and resend it.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

SYSTEM = (
    "You are an on-call assistant for a Windows infrastructure team. "
    "Be concise. If you don't know, say so."
)

history = []

print("On-call bot (type 'exit' to quit)")
while True:
    user_text = input("\nyou> ").strip()
    if user_text.lower() in {"exit", "quit"}:
        break
    if not user_text:
        continue

    history.append({"role": "user", "content": user_text})

    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        temperature=0,
        system=SYSTEM,
        messages=history,
    )
    reply = resp.content[0].text
    print(f"bot> {reply}")

    # IMPORTANT: append assistant turn so next call has full context
    history.append({"role": "assistant", "content": reply})
