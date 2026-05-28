"""
Phase 3.4 - Prefilling for hard format guarantees.

Pattern: put the start of the format in the assistant turn so the model
has to continue from there.

Three demos:
1. Force JSON open brace
2. Force a numbered-list start
3. Force a code fence with a chosen language
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def call(messages, max_tokens=400):
    return client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=max_tokens,
        temperature=0,
        messages=messages,
    ).content[0].text


# 1. JSON
print("--- JSON via prefill ---")
print("{" + call([
    {"role": "user", "content": 'Return {"city":..., "country":...} for Tokyo.'},
    {"role": "assistant", "content": "{"},
]))

# 2. Numbered list
print("\n--- Numbered list via prefill ---")
print("1." + call([
    {"role": "user", "content": "List 3 reasons to use MFA."},
    {"role": "assistant", "content": "1."},
]))

# 3. PowerShell code fence
print("\n--- PowerShell code via prefill ---")
print("```powershell\n" + call([
    {"role": "user", "content": "Write a PowerShell one-liner to list disabled AD users."},
    {"role": "assistant", "content": "```powershell\n"},
]))
