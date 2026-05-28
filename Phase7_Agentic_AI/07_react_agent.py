"""
Phase 7.7 - Minimal autonomous ReAct agent with safety knobs.

Tools: list_files, read_file, count_lines.
Task : "How many total lines of Python are in this folder?"

The agent loops up to max_steps. We log every step.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

ROOT = Path(__file__).parent


def list_files(directory: str = "."):
    d = (ROOT / directory).resolve()
    return [str(p.relative_to(ROOT)) for p in d.glob("*.py")]


def read_file(path: str, max_chars: int = 4000):
    p = (ROOT / path).resolve()
    # safety: keep inside ROOT
    if ROOT not in p.parents and p != ROOT:
        return "ERROR: outside sandbox"
    return p.read_text(encoding="utf-8")[:max_chars]


def count_lines(path: str):
    return len(read_file(path).splitlines())


DISPATCH = {"list_files": list_files, "read_file": read_file, "count_lines": count_lines}
TOOLS = [
    {"name": "list_files",
     "description": "List .py files in a directory relative to project root.",
     "input_schema": {"type": "object",
                      "properties": {"directory": {"type": "string"}}}},
    {"name": "read_file",
     "description": "Read up to 4000 chars of a text file.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}},
                      "required": ["path"]}},
    {"name": "count_lines",
     "description": "Count lines in a text file.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}},
                      "required": ["path"]}},
]

SYSTEM = ("You are a careful coding agent. Use the smallest number of tool calls "
          "needed. When you have the final answer, reply in plain text - no tools.")


def react(question: str, max_steps: int = 8):
    messages = [{"role": "user", "content": question}]
    total_in = total_out = 0
    for step in range(max_steps):
        r = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )
        total_in += r.usage.input_tokens
        total_out += r.usage.output_tokens
        if r.stop_reason != "tool_use":
            txt = next(b.text for b in r.content if b.type == "text")
            print(f"\n[done step {step}] tokens in/out={total_in}/{total_out}")
            return txt
        messages.append({"role": "assistant", "content": r.content})
        results = []
        for blk in r.content:
            if blk.type == "tool_use":
                print(f"step {step}  tool {blk.name} {blk.input}")
                try:
                    out = DISPATCH[blk.name](**blk.input)
                except Exception as e:
                    out = f"ERROR: {e}"
                results.append({"type": "tool_result",
                                "tool_use_id": blk.id,
                                "content": str(out)[:4000]})
        messages.append({"role": "user", "content": results})
    return "[max_steps reached]"


if __name__ == "__main__":
    print(react("How many total lines of Python are in this folder?"))
