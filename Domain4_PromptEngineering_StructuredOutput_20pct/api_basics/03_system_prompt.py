"""
Phase 2.3 - System prompt + temperature.

Real-world: same user question, three different system prompts.
Watch how the persona changes the answer without changing the user text.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

USER = "Our DC sync is failing. What do I do?"

PERSONAS = {
    "Senior AD Engineer": (
        "You are a senior Active Directory engineer. Give 3 numbered, "
        "specific troubleshooting steps with exact PowerShell commands."
    ),
    "Empathetic Helpdesk L1": (
        "You are an empathetic L1 helpdesk agent. Acknowledge stress first, "
        "then ask ONE clarifying question. Do not give technical commands."
    ),
    "Strict Security Auditor": (
        "You are a strict security auditor. Reply ONLY with a JSON object: "
        '{"risk":"low|medium|high","next_action":"..."}.'
    ),
}

for name, system in PERSONAS.items():
    print(f"\n=== Persona: {name} ===")
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": USER}],
    )
    print(resp.content[0].text)
