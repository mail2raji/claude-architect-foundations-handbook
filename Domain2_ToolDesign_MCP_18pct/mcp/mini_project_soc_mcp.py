"""
Phase 6 mini-project - SOC analyst MCP server.

Tools:    query_sentinel(kql), close_incident(id, reason)
Resource: sentinel://incident/{id}    (incident JSON)
Prompt:   /triage-incident severity=high

You can plug this into Claude Desktop or call it from your own client.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("soc-server")

INCIDENTS = {
    "INC-001": {
        "id": "INC-001", "severity": "high", "title": "Suspicious outbound traffic",
        "rule": "outbound-c2-block",
        "raw": "src=10.0.4.22 dst=185.244.25.7 dport=4444 action=DENY",
        "status": "open",
    },
    "INC-002": {
        "id": "INC-002", "severity": "low", "title": "Failed sign-in (single)",
        "rule": "sign-in-anomaly", "raw": "user=tester1 country=Nigeria result=fail",
        "status": "open",
    },
}


# ---- tools ---------------------------------------------------------------
@mcp.tool()
def query_sentinel(kql: str) -> list:
    """Run a KQL query against Sentinel and return incidents (mocked).
    For demo: returns all OPEN incidents matching keyword in kql."""
    keyword = "high" if "high" in kql.lower() else ""
    return [i for i in INCIDENTS.values()
            if i["status"] == "open" and (not keyword or i["severity"] == keyword)]


@mcp.tool()
def close_incident(incident_id: str, reason: str) -> dict:
    """Close an incident with a reason."""
    if incident_id not in INCIDENTS:
        return {"error": "not found"}
    INCIDENTS[incident_id]["status"] = "closed"
    INCIDENTS[incident_id]["close_reason"] = reason
    return {"ok": True, "id": incident_id, "status": "closed"}


# ---- resource ------------------------------------------------------------
@mcp.resource("sentinel://incident/{incident_id}")
def get_incident(incident_id: str) -> dict:
    """Fetch an incident document by id."""
    return INCIDENTS.get(incident_id, {"error": "not found"})


# ---- prompt --------------------------------------------------------------
@mcp.prompt()
def triage_incident(severity: str = "medium") -> str:
    """Pre-canned triage workflow."""
    return (
        f"You are a SOC tier-2 analyst. Severity={severity}. "
        "Steps: 1) Call query_sentinel to enumerate open incidents. "
        "2) For each, hypothesize root cause. 3) If false-positive, "
        "call close_incident with a clear reason. 4) Summarize actions."
    )


if __name__ == "__main__":
    mcp.run()
