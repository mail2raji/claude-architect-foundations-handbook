"""
Phase 0 - Your first Claude API call.

Real-world framing: you are an IT admin who wants Claude to summarize a
firewall log line. We pass the log line and ask for a one-sentence summary.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()  # picks up ANTHROPIC_API_KEY from env

log_line = (
    "2026-05-28 03:14:11 BLOCK src=10.0.4.22 dst=185.244.25.7 "
    "proto=TCP dport=4444 action=DENY rule=outbound-c2-block"
)

response = client.messages.create(
    model="claude-sonnet-4-5",       # safe, current default
    max_tokens=200,
    system="You are a senior SOC analyst. Reply in ONE plain English sentence.",
    messages=[
        {"role": "user", "content": f"Summarize this firewall log:\n{log_line}"}
    ],
)

print("Model:", response.model)
print("Stop reason:", response.stop_reason)
print("Reply :", response.content[0].text)
print("Input tokens :", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)
