"""
Domain 2 — Tool Design & Model Context Protocol (18% of the cert)
==================================================================
A SINGLE step-by-step walkthrough covering both Domain 2 halves:
  - Tool design  (sub-folder tool_use/)
  - MCP servers  (sub-folder mcp/)

Run with:
    python Domain2_ToolDesign_MCP_18pct/lab_walkthrough.py

STEPS:
    STEP 1 — Write tool descriptions that disambiguate (Lab 2.1).
    STEP 2 — Return STRUCTURED errors, not free-text strings (Lab 2.2).
    STEP 3 — Choose the right `tool_choice` mode (Lab 2.3).
    STEP 4 — Least-privilege tool allocation per agent role (Lab 2.4).
    STEP 5 — Mental model of an MCP server (Lab 2.5 — design only).
    STEP 6 — Configure MCP servers correctly (Lab 2.6).
    STEP 7 — Built-in tool selection drill (Lab 2.7).

This file is intentionally NETWORK-FREE — every step is exercised through
dictionaries and assertions so you can re-read the patterns without burning
API tokens. Run real API examples from 02_tool_use_basics.py and 03_mcp_*.py.
"""

from __future__ import annotations
import json


def banner(step: int, title: str) -> None:
    print(f"\n{'=' * 70}\n=== STEP {step}: {title}\n{'=' * 70}")


# ---------------------------------------------------------------------------
# STEP 1 — Disambiguating tool descriptions (Lab 2.1)
# ---------------------------------------------------------------------------
banner(1, "Tool descriptions must disambiguate from peers (Lab 2.1)")

BAD_TOOL = {
    "name": "search",
    "description": "Search.",     # useless: cannot tell which 'search' to use
    "input_schema": {"type": "object", "properties": {"q": {"type": "string"}}},
}

GOOD_TOOLS = [
    {
        "name": "search_internal_kb",
        "description": (
            "Search ONLY the internal knowledge base (policies, runbooks, post-mortems). "
            "Use BEFORE web_search if the question is about company-specific procedures. "
            "Returns up to 5 matching documents with title, URL, and snippet."
        ),
        "input_schema": {"type": "object", "properties": {
            "query": {"type": "string", "description": "Search terms; do NOT include the word 'internal'."},
            "max_results": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20},
        }, "required": ["query"]},
    },
    {
        "name": "search_web",
        "description": (
            "Search the public web. Use ONLY when search_internal_kb returns nothing "
            "or for time-sensitive news. Returns 10 results with title/URL/snippet."
        ),
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}},
                         "required": ["query"]},
    },
]
print("Compare description quality:")
print(f"  BAD :  {BAD_TOOL['description']!r}")
for t in GOOD_TOOLS:
    print(f"  GOOD:  {t['name']}: {t['description'][:80]}...")
print("""
RULE: write descriptions for a NEW EMPLOYEE who has never seen your codebase.
State (a) what it does, (b) when to use it, (c) when NOT to use it,
       (d) the shape of the return value.
""")


# ---------------------------------------------------------------------------
# STEP 2 — Structured tool errors (Lab 2.2)
# ---------------------------------------------------------------------------
banner(2, "Structured errors enable retry/repair (Lab 2.2)")

BAD_ERROR = "ERROR: something went wrong"   # the agent cannot reason about this

GOOD_ERROR = {
    "is_error": True,
    "error_code": "RATE_LIMITED",
    "retryable": True,
    "retry_after_seconds": 30,
    "message": "Upstream API rate limit hit (HTTP 429).",
    "remediation": "Wait the suggested seconds, then retry the same call.",
}
print(f"  BAD  : {BAD_ERROR}")
print(f"  GOOD : {json.dumps(GOOD_ERROR, indent=2)}")
print("""
With structured errors the agent can:
  - retry transient failures (retryable=true) without asking the user
  - explain to the user WHY a permanent failure happened
  - choose a DIFFERENT tool if remediation says so
""")


# ---------------------------------------------------------------------------
# STEP 3 — tool_choice modes (Lab 2.3)
# ---------------------------------------------------------------------------
banner(3, "tool_choice: auto vs any vs tool vs none (Lab 2.3)")
MODES = {
    "auto":  "Default. Claude decides whether to call any tool, multiple, or none.",
    "any":   "FORCE at least one tool call. Risk: model may pick a wrong tool to satisfy the constraint.",
    "tool":  "Force ONE specific tool. Use for tool-as-formatter (strict JSON).",
    "none":  "Disable all tools for this turn. Use when you want a clean natural-language reply.",
}
for k, v in MODES.items():
    print(f"  tool_choice={k:6} -> {v}")
print("""
DECISION TREE:
  - Need free-form reasoning? -> auto
  - Need a specific schema?   -> tool (with one tool defined as the formatter)
  - Need to guarantee SOME tool runs (e.g. classifier)? -> any (last resort)
  - Need plain prose, no tool noise? -> none
""")


# ---------------------------------------------------------------------------
# STEP 4 — Least-privilege per role (Lab 2.4)
# ---------------------------------------------------------------------------
banner(4, "Least-privilege tool allocation (Lab 2.4)")

ALL_TOOLS = ["read_doc", "search_kb", "send_email", "delete_customer", "create_ticket"]

ROLE_ALLOWLISTS = {
    "researcher":      ["read_doc", "search_kb"],
    "support_agent":   ["read_doc", "search_kb", "create_ticket"],
    "billing_admin":   ["read_doc", "search_kb", "create_ticket", "send_email"],
    # delete_customer is NOT in any role -- it requires a human in the loop.
}
for role, allowed in ROLE_ALLOWLISTS.items():
    denied = sorted(set(ALL_TOOLS) - set(allowed))
    print(f"  {role:14}  ALLOW: {allowed}\n                  DENY : {denied}\n")
print("""
PRINCIPLE: the blast radius of a prompt-injection attack is bounded by the
union of tools available to the compromised agent. Give each agent the
narrowest list that lets it do its job.
""")


# ---------------------------------------------------------------------------
# STEP 5 — Mental model of an MCP server (Lab 2.5)
# ---------------------------------------------------------------------------
banner(5, "MCP primitives: tools / resources / prompts (Lab 2.5)")
print("""
The Model Context Protocol exposes three primitive kinds, each with a
distinct ownership model:

  TOOLS     -> model-controlled. Claude decides when to call.
               Example: 'create_ticket(title, body)'.

  RESOURCES -> app-controlled. The host app attaches them to context.
               Example: 'crm://account/{id}' fetches that account's dossier.

  PROMPTS   -> user-controlled. User invokes by name (slash command).
               Example: '/quarterly_account_brief account_id=42'.

TRANSPORTS:
  stdio              -> local subprocess. One client, simplest auth.
  streamable HTTP    -> remote server. Supports multiple clients + OAuth.
""")
MIN_MCP_SERVER_SKELETON = """
# pip install mcp
from mcp.server.fastmcp import FastMCP
server = FastMCP("my-crm")

@server.tool()
def search_accounts(query: str) -> list[dict]:
    return crm.search(query)

@server.resource("crm://account/{account_id}")
def account_dossier(account_id: str) -> str:
    return crm.dossier(account_id)

@server.prompt()
def quarterly_account_brief(account_id: str) -> str:
    return f"Draft a quarterly brief for account {account_id}."

if __name__ == '__main__':
    server.run()
"""
print(MIN_MCP_SERVER_SKELETON)


# ---------------------------------------------------------------------------
# STEP 6 — Configure MCP servers (Lab 2.6)
# ---------------------------------------------------------------------------
banner(6, "MCP server configuration (Lab 2.6)")
CONFIG_EXAMPLE = {
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/safe/sandbox/path"],
            # least-privilege: limit FS scope, never point at $HOME or /
        },
        "company-crm": {
            "type": "http",
            "url": "https://mcp.example.com",
            "headers": {"Authorization": "Bearer ${CRM_TOKEN}"},
        },
    }
}
print(json.dumps(CONFIG_EXAMPLE, indent=2))
print("""
COMMON MISTAKES:
  - Filesystem server pointed at $HOME (= full disk access via prompt injection).
  - HTTP server with no auth header (= anyone on the LAN can use your tools).
  - Hard-coded secrets in config (use env-var interpolation like ${VAR}).
""")


# ---------------------------------------------------------------------------
# STEP 7 — Built-in tool selection drill (Lab 2.7)
# ---------------------------------------------------------------------------
banner(7, "Pick the built-in tool for each job (Lab 2.7)")
DRILL = [
    ("Run a small Python snippet to compute a tricky number",   "code_execution"),
    ("Get today's NBA scores",                                   "web_search"),
    ("Read the PDF the user just uploaded",                      "file (input)"),
    ("Click through a flaky web form to file a ticket",          "computer_use (CAUTION: full UI access)"),
    ("Strict JSON for a 7-class classifier",                     "tool_use as formatter (your own tool)"),
]
for job, answer in DRILL:
    print(f"  Q: {job}\n    -> {answer}\n")


# ---------------------------------------------------------------------------
# SELF-CHECK
# ---------------------------------------------------------------------------
print(f"\n{'=' * 70}\n=== SELF-CHECK\n{'=' * 70}")
print("""
  1. Four things a good tool description must contain?
  2. What FIELD on a tool_result enables retry-with-feedback?
  3. Pick tool_choice for: 'force the model to emit a 7-enum label as JSON'.
  4. What is the bound on prompt-injection blast radius?
  5. Name the 3 MCP primitives and who controls each.
  6. Name the 2 MCP transports and when to pick each.
  7. Why is pointing the filesystem MCP server at $HOME dangerous?

When you can answer all 7 from memory, tick the checklist in
  Domain2_ToolDesign_MCP_18pct/tool_use/exam_prep/final_checklist.md
  Domain2_ToolDesign_MCP_18pct/mcp/exam_prep/final_checklist.md
""")
