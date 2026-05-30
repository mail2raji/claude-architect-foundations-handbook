"""
Phase 6.4 - Bridge MCP tools to Claude.

We:
  1. Connect to the MCP server.
  2. Call list_tools(); convert each MCP tool definition into Anthropic
     tool-schema shape.
  3. Run a tool-use loop with Claude where, whenever Claude requests
     a tool, we dispatch the call through MCP.

This is exactly how Claude Desktop and Claude Code bridge MCP servers.
"""

import asyncio
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
claude = Anthropic()
SERVER_PATH = Path(__file__).parent / "02_mcp_server.py"


def mcp_tool_to_anthropic(t):
    """Translate an MCP tool definition into the Anthropic schema."""
    return {
        "name": t.name,
        "description": t.description or "",
        "input_schema": t.inputSchema or {"type": "object", "properties": {}},
    }


async def run_agent(question: str):
    params = StdioServerParameters(command="python", args=[str(SERVER_PATH)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            anthropic_tools = [mcp_tool_to_anthropic(t) for t in mcp_tools]
            print("Bridging tools:", [t["name"] for t in anthropic_tools])

            messages = [{"role": "user", "content": question}]
            for _ in range(6):
                resp = claude.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=800,
                    tools=anthropic_tools,
                    messages=messages,
                )
                if resp.stop_reason != "tool_use":
                    print("\n>>>", next(b.text for b in resp.content if b.type == "text"))
                    return
                messages.append({"role": "assistant", "content": resp.content})
                results = []
                for blk in resp.content:
                    if blk.type == "tool_use":
                        print(f"[MCP] {blk.name}({blk.input})")
                        mcp_result = await session.call_tool(blk.name, blk.input)
                        text = mcp_result.content[0].text if mcp_result.content else ""
                        results.append({
                            "type": "tool_result",
                            "tool_use_id": blk.id,
                            "content": text,
                        })
                messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    asyncio.run(run_agent("Is employee E2050 currently active? Just yes or no."))
