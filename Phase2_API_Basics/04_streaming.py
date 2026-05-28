"""
Phase 2.4 - Streaming responses.

Real-world: a chat UI where the user wants to see Claude "typing".
Without streaming, the user stares at a spinner for several seconds.
With streaming, they see the answer appear token-by-token.

We print the running text to stdout as it arrives.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=400,
    system="You explain technical topics to beginners.",
    messages=[
        {"role": "user", "content": "Explain Active Directory replication in 5 short bullets."}
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

    # When the stream ends, you can still get the full message
    final = stream.get_final_message()
    print("\n\n--- done ---")
    print("usage:", final.usage)
    print("stop_reason:", final.stop_reason)
