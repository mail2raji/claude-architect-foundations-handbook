"""
Phase 2.7 - Stop reasons, retries, errors.

Real-world: production code MUST handle rate limits, timeouts, and
'max_tokens' truncation gracefully.

We show:
- Catching anthropic.RateLimitError and APIError
- Detecting stop_reason == 'max_tokens' and continuing
- Exponential backoff helper
"""

import time
from dotenv import load_dotenv
from anthropic import Anthropic, RateLimitError, APIStatusError

load_dotenv()
client = Anthropic()


def call_with_retry(messages, system="", max_tokens=400, retries=4):
    """Tiny retry helper with exponential backoff."""
    for attempt in range(retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=max_tokens,
                system=system,
                messages=messages,
            )
        except RateLimitError:
            wait = 2 ** attempt
            print(f"[rate-limit] retry in {wait}s")
            time.sleep(wait)
        except APIStatusError as e:
            if e.status_code >= 500 and attempt < retries - 1:
                wait = 2 ** attempt
                print(f"[5xx] retry in {wait}s ({e.status_code})")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("Exceeded retries")


def generate_long_essay(topic, budget_tokens=2000):
    """Keep continuing the response until model stops naturally or budget hit."""
    messages = [{"role": "user", "content": f"Write a long essay about {topic}."}]
    used = 0
    full = ""
    while used < budget_tokens:
        # ask for a chunk
        chunk_tokens = min(400, budget_tokens - used)
        resp = call_with_retry(messages, max_tokens=chunk_tokens)
        chunk_text = resp.content[0].text
        full += chunk_text
        used += resp.usage.output_tokens

        if resp.stop_reason == "end_turn":
            break
        if resp.stop_reason == "max_tokens":
            # ask Claude to continue
            messages.append({"role": "assistant", "content": chunk_text})
            messages.append({"role": "user", "content": "continue"})
            continue
        break
    return full


if __name__ == "__main__":
    essay = generate_long_essay("Kerberos authentication in 200 words", budget_tokens=600)
    print(essay)
