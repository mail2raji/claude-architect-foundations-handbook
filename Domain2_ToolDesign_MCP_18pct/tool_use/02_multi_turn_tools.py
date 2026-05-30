"""
Phase 4.2 - Generic agent loop that handles N tool turns.

Pattern: keep looping until stop_reason != 'tool_use'. This is the
SAME loop you'll reuse in every later agent example.
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# A registry of {tool_name: python_callable}
def add(a: float, b: float): return {"result": a + b}
def multiply(a: float, b: float): return {"result": a * b}
def square_root(x: float): return {"result": x ** 0.5}

TOOLS = [
    {"name": "add",         "description": "Add two numbers.",
     "input_schema": {"type": "object",
                      "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                      "required": ["a", "b"]}},
    {"name": "multiply",    "description": "Multiply two numbers.",
     "input_schema": {"type": "object",
                      "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                      "required": ["a", "b"]}},
    {"name": "square_root", "description": "Square root of x.",
     "input_schema": {"type": "object",
                      "properties": {"x": {"type": "number"}},
                      "required": ["x"]}},
]
DISPATCH = {"add": add, "multiply": multiply, "square_root": square_root}


def run_agent(user_msg: str, max_turns: int = 6) -> str:
    messages = [{"role": "user", "content": user_msg}]
    for turn in range(max_turns):
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        if resp.stop_reason != "tool_use":
            # final answer reached
            return next(b.text for b in resp.content if b.type == "text")

        # otherwise execute every tool_use block in this response
        messages.append({"role": "assistant", "content": resp.content})
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                fn = DISPATCH[block.name]
                try:
                    out = fn(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(out),
                    })
                except Exception as e:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"ERROR: {e}",
                        "is_error": True,
                    })
        messages.append({"role": "user", "content": tool_results})
    return "[agent hit max_turns without finishing]"


if __name__ == "__main__":
    q = "Compute the square root of (3.5 * 2 + 7.25). Show me the answer only."
    print(run_agent(q))
