"""
Phase 2.1 - Single-turn request and reading the response object.

Real-world: an HR bot that classifies an incoming email as Leave / Payroll /
Other.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

email = """
Subject: time off
Hi, I need 3 days off next week for a family event.  Please confirm.
"""

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=50,
    temperature=0,
    system="You classify emails. Reply with ONE word: Leave, Payroll, or Other.",
    messages=[{"role": "user", "content": email}],
)

# The response object
print("id         :", resp.id)
print("model      :", resp.model)
print("role       :", resp.role)
print("stop_reason:", resp.stop_reason)
print("usage      :", resp.usage)

# `content` is a list of content blocks. For pure text, take index 0.
print("category   :", resp.content[0].text)
