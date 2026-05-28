"""
Phase 4.5 - Anthropic-hosted built-in tool: web_search.

You enable it by adding it to tools=[]. Claude executes the search
server-side; you don't run anything. The result blocks come back as
normal content.

NOTE: web_search may require a beta header on some accounts. If you
get a 4xx mentioning beta, add it as shown.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=800,
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 3,
        }
    ],
    # extra_headers={"anthropic-beta": "web-search-2025-03-05"},  # if needed
    messages=[{
        "role": "user",
        "content": "What were the top 3 announcements at Microsoft Build 2026? Cite sources."
    }],
)

# Print final text + any citations
for block in resp.content:
    if block.type == "text":
        print(block.text)
