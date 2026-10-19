"""MCP server for Incident Severity Assessor & Escalation Matrix."""
import sys
import json
from client import IncidentSeverityCoordinator


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "assess_incident_severity",
                    "description": "Calculates standardized severity (SEV0-SEV3), SLA response windows, and coordinates on-call escalation paging",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "impact_metrics": {
                                "type": "object",
                                "description": "Metrics containing affected_users_percentage, core_revenue_flow_down, and data_loss_or_corruption",
                            },
                            "incident_description": {"type": "string"},
                        },
                        "required": ["impact_metrics", "incident_description"],
                    },
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "assess_incident_severity":
            res = IncidentSeverityCoordinator.assess_incident(
                args.get("impact_metrics", {}),
                args.get("incident_description", ""),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
