"""
Phase 6.3 - MCP client.

Launches the server (02_mcp_server.py) as a subprocess over stdio,
lists everything it offers, and invokes one of each primitive.
"""

import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = Path(__file__).parent / "02_mcp_server.py"


async def main():
    params = StdioServerParameters(command="python", args=[str(SERVER_PATH)])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # ---- enumerate ----
            tools = (await session.list_tools()).tools
            print("Tools:", [t.name for t in tools])

            res = (await session.list_resource_templates()).resourceTemplates
            print("Resource templates:", [r.uriTemplate for r in res])

            prompts = (await session.list_prompts()).prompts
            print("Prompts:", [p.name for p in prompts])

            # ---- invoke tool ----
            r = await session.call_tool("get_employee_status", {"employee_id": "E1042"})
            print("\nTool result:", r.content[0].text)

            # ---- read resource ----
            rr = await session.read_resource("policy://password")
            print("\nPolicy:", rr.contents[0].text)

            # ---- get prompt ----
            pr = await session.get_prompt("incident_triage", {"severity": "high"})
            print("\nPrompt messages:")
            for m in pr.messages:
                print(f"  [{m.role}] {m.content.text[:120]}...")


if __name__ == "__main__":
    asyncio.run(main())
