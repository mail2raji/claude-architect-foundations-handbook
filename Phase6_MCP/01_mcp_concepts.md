# MCP Concepts Cheat-Sheet

## The three primitives

| Primitive | Who decides to use it? | Looks like | Use for |
|---|---|---|---|
| **Tool** | The MODEL (Claude) | Function call w/ JSON args | Actions: create_ticket, run_query |
| **Resource** | The APP/USER (client UI) | URI like `notion://page/123` | Data the user picks: docs, rows |
| **Prompt** | The USER (slash-command) | Named template, optional args | Pre-canned workflows |

## Lifecycle

1. Client launches server (stdio or HTTP).
2. `initialize` handshake — exchange capabilities and protocol version.
3. Client calls `list_tools`, `list_resources`, `list_prompts`.
4. As the user/model interacts:
   - Model decides to call a tool → `call_tool(name, args)`.
   - User picks a resource → `read_resource(uri)`.
   - User picks a prompt → `get_prompt(name, args)` → server returns messages.
5. `shutdown` when done.

## Transports

| Transport | When to use |
|---|---|
| **stdio** | Local dev, Claude Desktop, Claude Code |
| **Streamable HTTP** | Remote / multi-tenant, cloud |
| (Legacy SSE) | Older clients |

## Capabilities flag

Each server announces what it supports in `initialize`:
- `tools`
- `resources` (and whether they're `subscribe`-able)
- `prompts`
- `logging`
- `sampling` (server asking the client's model to do an LLM call — "reverse" direction)

## Common gotchas

- Tool descriptions are what the MODEL reads. Be precise.
- Resource URIs are arbitrary strings — pick a clean scheme (`my://...`).
- Errors should be returned as `is_error` payloads, not raised across the wire.
- Resources can be **subscribed** to for live updates (e.g., file watcher).

## Where to learn more
- Spec: https://modelcontextprotocol.io
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Reference servers: https://github.com/modelcontextprotocol/servers
