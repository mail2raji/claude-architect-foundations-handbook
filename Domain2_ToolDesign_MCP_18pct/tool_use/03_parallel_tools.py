"""
Phase 4.3 - Parallel tool use.

Claude can request multiple tool calls in a SINGLE response (multiple
tool_use blocks). Your runner should execute them concurrently for
latency wins.

Demo: ask 'compare weather in Tokyo, Mumbai, and London'. Claude will
issue three get_weather calls at once.
"""

import concurrent.futures as cf
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

TOOL = {
    "name": "get_weather",
    "description": "Current weather for a city.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}

def get_weather(city: str):
    fake = {"Tokyo": (24, "Cloudy"), "Mumbai": (33, "Humid"), "London": (12, "Rainy")}
    t, s = fake.get(city, (20, "Pleasant"))
    return {"city": city, "temp_c": t, "summary": s}


messages = [{"role": "user",
             "content": "Compare today's weather in Tokyo, Mumbai, and London. One line each."}]

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[TOOL],
    messages=messages,
)

if resp.stop_reason == "tool_use":
    messages.append({"role": "assistant", "content": resp.content})
    tool_blocks = [b for b in resp.content if b.type == "tool_use"]
    print(f"Claude requested {len(tool_blocks)} parallel tool calls")

    # Run them concurrently
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        future_map = {ex.submit(get_weather, **b.input): b for b in tool_blocks}
        results = []
        for fut in cf.as_completed(future_map):
            blk = future_map[fut]
            results.append({
                "type": "tool_result",
                "tool_use_id": blk.id,
                "content": str(fut.result()),
            })

    messages.append({"role": "user", "content": results})
    final = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=600,
        tools=[TOOL],
        messages=messages,
    )
    print(final.content[0].text)
