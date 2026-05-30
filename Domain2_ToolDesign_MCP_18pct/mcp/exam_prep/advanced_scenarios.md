# Advanced Architectural Scenarios — Domain 2b — Model Context Protocol (part of Domain 2, 18%)

Sourced from the consolidated 25 cross-domain scenarios.
Only the **1 scenarios tagged for this domain** appear here.

Sketch an architecture answer first, then compare to the solution sketch at the bottom.

---

## Exercises

**E13.** A startup wants to expose its internal CRM as MCP so multiple Claude clients can query it. Architect the MCP server.


---
## Solution sketches

**A13.** FastMCP server. Tools: `search_accounts`, `get_opportunity`, `update_note`. Resources: per-account contact dossier as `crm://account/{id}`. Prompt: `quarterly_account_brief`. Streamable HTTP transport. Auth via OAuth bearer.
