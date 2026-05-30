"""
Phase 6.2 - MCP server with one tool, one resource, one prompt.

Run it directly to start the stdio server. Easier: let the client
in 03_mcp_client.py launch this file as a subprocess.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo-server")

# ---- tool (model controls) ------------------------------------------------
@mcp.tool()
def get_employee_status(employee_id: str) -> dict:
    """Look up an employee's status by ID. Returns name, dept, is_active."""
    db = {
        "E1042": {"name": "Priya Subramanian", "dept": "Finance",  "is_active": True},
        "E2050": {"name": "Mark Cohen",        "dept": "Marketing","is_active": False},
    }
    return db.get(employee_id, {"error": "unknown"})


# ---- resource (app/user controls) -----------------------------------------
POLICIES = {
    "password": "Passwords must be 14+ chars, rotated every 365 days.",
    "vpn":      "VPN required for any access outside corp network.",
}

@mcp.resource("policy://{name}")
def get_policy(name: str) -> str:
    """Read a corporate policy by short name (e.g. 'password')."""
    return POLICIES.get(name, "policy not found")


# ---- prompt (user controls) -----------------------------------------------
@mcp.prompt()
def incident_triage(severity: str = "medium") -> str:
    """Pre-canned incident triage prompt."""
    return (
        f"You are a SOC tier-2 analyst. The user will paste an incident summary. "
        f"Treat it as severity={severity}. Output: 1) root cause hypothesis, "
        f"2) immediate containment actions, 3) follow-up checks."
    )


if __name__ == "__main__":
    mcp.run()    # stdio
