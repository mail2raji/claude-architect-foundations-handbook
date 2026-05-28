# Phase 6 — Exercises

1. Modify `02_mcp_server.py` to also expose a **subscribable resource** (`policy://*`) that emits an `updated` notification when the file changes.
2. Add an `is_error: True` path to a tool when invalid input arrives — and watch Claude correct itself in `04_bridge_mcp_to_claude.py`.
3. Wire `mini_project_soc_mcp.py` into Claude Desktop by editing `%APPDATA%\Claude\claude_desktop_config.json`. Confirm the tools appear in Claude Desktop.
4. Write a second MCP server `02b_kb_server.py` (RAG over the Phase 5 KB) and connect BOTH servers in `04_bridge_mcp_to_claude.py` simultaneously.

## Mini quiz

1. In MCP, who decides when a **tool** runs vs when a **resource** is read vs when a **prompt** is used?
2. What are the two main MCP transports?
3. What is the `initialize` step?
4. Why is "tool description quality" so important in MCP?
5. Name one MCP capability beyond tools/resources/prompts.

### Answers
1. **Tool** = model; **Resource** = app/user; **Prompt** = user.
2. **stdio** (subprocess) and **Streamable HTTP** (network).
3. The handshake where client and server exchange capabilities and protocol versions before any other call.
4. The model only sees the *description* when deciding to call a tool. Bad description → wrong call.
5. `logging`, `sampling` (server asks the client's model to do an LLM call), resource `subscribe`.
