# Phase 6 — Model Context Protocol (MCP)

**Maps to:** Skilljar "Model Context Protocol (MCP)" (12 lessons) + the dedicated **MCP fundamentals** course (16 lessons). **Exam weight: ~10%.**
**Goal:** Build and consume MCP **servers** and **clients** so any Claude app can plug in your data and tools without bespoke glue code.

---

## 6.1 Why MCP exists

Imagine you've built five Claude apps. Each one needs a `search_jira` tool, a `read_sharepoint` tool, etc. You're now re-implementing the same tool wrappers in every app. MCP standardizes that:

- A **server** exposes **tools**, **resources**, and **prompts** over a small protocol.
- A **client** (Claude Desktop, Claude Code, your custom app) **connects** to any MCP server.

Now every Claude app you write can plug in any MCP server in seconds. Think of MCP as **"USB-C for AI tools."**

---

## 6.2 The three MCP primitives

This is **the** exam question of Phase 6. Memorize.

| Primitive | Who controls? | Analogy | Examples |
|---|---|---|---|
| **Tool** | **Model** (Claude decides when to call) | Function call | `create_jira_ticket`, `send_slack_msg` |
| **Resource** | **Application/user** (the client surfaces them, user picks) | File / database row | `notion://page/123`, `db://customers/42` |
| **Prompt** | **User** (user picks a template) | Pre-canned slash-command | `/code-review`, `/summarize-meeting` |

Mnemonic: **T**ool = model. **R**esource = app/user. **P**rompt = user.

---

## 6.3 Architecture in one diagram

```
┌────────────────┐     stdio / HTTP+SSE     ┌──────────────────────┐
│                │ ◄───────────────────────►│                      │
│   MCP CLIENT   │   JSON-RPC over Streams  │     MCP SERVER       │
│  (Claude.ai,   │                          │   (your Python or    │
│   Claude Code, │   list_tools()           │    Node.js process)  │
│   custom app)  │   call_tool(name, args)  │                      │
│                │   list_resources()       │   @mcp.tool          │
│                │   read_resource(uri)     │   @mcp.resource      │
│                │   list_prompts()         │   @mcp.prompt        │
│                │   get_prompt(name)       │                      │
└────────────────┘                          └──────────────────────┘
```

Two transports you must know:
- **stdio** — server runs as a subprocess of the client (most common; what Claude Desktop uses).
- **HTTP + SSE / Streamable HTTP** — server runs as a network service (for remote / multi-tenant).

---

## 6.4 Minimum viable Python MCP server

Anthropic's `mcp` Python SDK uses `FastMCP`:

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.resource("docs://policy/{name}")
def get_policy(name: str) -> str:
    """Return policy text by name."""
    return open(f"policies/{name}.md").read()

@mcp.prompt()
def code_review(language: str = "python") -> str:
    """Pre-canned code review prompt."""
    return f"You are a senior {language} reviewer. Be strict but kind."

if __name__ == "__main__":
    mcp.run()    # stdio by default
```

That's a complete MCP server. You can hand the file to a friend, they add it to their Claude Desktop config, and suddenly Claude can call `add()` for them.

---

## 6.5 Connecting Claude Desktop / Claude Code

You add it to the client's config file:

```jsonc
// %APPDATA%\Claude\claude_desktop_config.json (Windows)
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["C:\\Scripts\\Send-escalationEmail\\Claude_Learning\\Phase6_MCP\\02_mcp_server.py"]
    }
  }
}
```

Restart the client and the tool appears. Same JSON shape works in Claude Code.

---

## 6.6 MCP client from scratch (when you build your own app)

Skip the desktop — talk to the server programmatically:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(command="python", args=["02_mcp_server.py"])
async with stdio_client(params) as (read, write):
    async with ClientSession(read, write) as s:
        await s.initialize()
        tools = await s.list_tools()
        result = await s.call_tool("add", {"a": 1, "b": 2})
```

We implement this end-to-end in `03_mcp_client.py` and then **bridge it to Claude** — every MCP tool gets auto-registered as an Anthropic tool in `04_bridge_mcp_to_claude.py`. That bridge is the secret sauce of every "agent that has an MCP server".

---

## 6.7 Real-world scenario

> **A SOC analyst chatbot** that should be able to:
> - Query Sentinel via KQL (a `query_sentinel(kql)` tool)
> - Read a specific incident as a resource (`sentinel://incident/{id}`)
> - Apply a "triage-incident" pre-canned prompt
>
> By making this an MCP server, the SAME server works in Claude Desktop for ad-hoc use, in your Python automation app, in Claude Code while developing — zero duplication. You build the toy version in `mini_project_soc_mcp.py`.

---

## 6.8 Hands-on examples

| # | File | Topic |
|---|---|---|
| 1 | [`01_mcp_concepts.md`](01_mcp_concepts.md) | Cheat-sheet of primitives & lifecycle |
| 2 | [`02_mcp_server.py`](02_mcp_server.py) | Working stdio server with tool + resource + prompt |
| 3 | [`03_mcp_client.py`](03_mcp_client.py) | Async client that lists & calls everything |
| 4 | [`04_bridge_mcp_to_claude.py`](04_bridge_mcp_to_claude.py) | Auto-register MCP tools as Anthropic tools |
| 5 | [`mini_project_soc_mcp.py`](mini_project_soc_mcp.py) | SOC analyst pattern |

### How to run

```powershell
cd Claude_Learning
.\.venv\Scripts\Activate.ps1
# Terminal 1: nothing — the client launches the server as a subprocess.
python Phase6_MCP\03_mcp_client.py
python Phase6_MCP\04_bridge_mcp_to_claude.py
```

---

## 6.9 Exercises & mini quiz → [`exercises.md`](exercises.md)

Next → [Phase 7: Agentic AI](../Phase7_Agentic_AI/README.md)
