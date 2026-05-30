# Harder Exercises — Domain 2b — Model Context Protocol (part of Domain 2, 18%)

Subset of the cross-domain 'harder exercises' file, filtered to this domain.
Each exercise expects an architect-level answer, not a tutorial-follower answer.

## (was Phase 6) MCP (harder)


**6H-1.** Build an MCP server that exposes 3 tools, 2 resources (URI-templated), and 1 prompt. Stand up a stdio client that calls each.

**6H-2.** Bridge your MCP server's tools to Claude. Add proper `is_error` propagation when a tool fails.

**6H-3.** Implement an MCP sampling capability where the server asks the client to do an LLM call. Use it for an "explain this incident in plain language" feature.

**6H-4.** Wrap your MCP server with auth (a bearer token). Refuse requests without it.

---
