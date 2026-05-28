"""
Phase 4.1 - The smallest possible tool-use loop.

Real-world: ask Claude for the current weather. Claude has no internet,
so it asks our tool. We return mock data. Claude weaves it into a reply.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

TOOL = {
    "name": "get_weather",
    "description": "Return the current weather (temp + summary) for a city.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. 'Tokyo'"},
            "units": {"type": "string", "enum": ["c", "f"], "default": "c"},
        },
        "required": ["city"],
    },
}

def get_weather(city: str, units: str = "c"):
    """Mock implementation - in real life you'd call an API."""
    fake = {"Tokyo": (24, "Cloudy"), "Mumbai": (33, "Humid"), "London": (12, "Rainy")}
    temp, summary = fake.get(city, (20, "Pleasant"))
    if units == "f":
        temp = round(temp * 9 / 5 + 32)
    return {"city": city, "temp": temp, "units": units, "summary": summary}


messages = [{"role": "user", "content": "What's the weather in Tokyo right now?"}]

# 1. First call - Claude probably asks for the tool
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    tools=[TOOL],
    messages=messages,
)
print("stop_reason:", resp.stop_reason)

if resp.stop_reason == "tool_use":
    # 2. Append the assistant turn EXACTLY as Claude returned it
    messages.append({"role": "assistant", "content": resp.content})

    # 3. Find the tool_use block, run our function
    tool_use = next(b for b in resp.content if b.type == "tool_use")
    print("Claude wants:", tool_use.name, tool_use.input)
    result = get_weather(**tool_use.input)
    print("We return  :", result)

    # 4. Send tool_result back as a user turn
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": str(result),
        }],
    })

    # 5. Second call - Claude weaves the answer
    final = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        tools=[TOOL],
        messages=messages,
    )
    print("\nFinal answer:", final.content[0].text)
