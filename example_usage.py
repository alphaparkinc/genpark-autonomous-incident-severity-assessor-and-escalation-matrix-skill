"""Example usage for Incident Severity Assessor & Escalation Matrix."""
from client import IncidentSeverityCoordinator

if __name__ == "__main__":
    metrics = {
        "affected_users_percentage": 65.0,
        "core_revenue_flow_down": True,
        "data_loss_or_corruption": False,
        "customer_facing": True,
    }

    res = IncidentSeverityCoordinator.assess_incident(
        impact_metrics=metrics,
        incident_description="Global Stripe payment webhook failure causing 100% of checkout payments to fail.",
    )

    print("Assigned Severity:", res["assigned_severity"], f"({res['severity_title']})")
    print("SLA Target:", res["sla_response_minutes"], "minutes")
    print("Escalation Target:", res["escalation_target"])
    print("Status Page Banner Required:", res["requires_status_page_banner"])
    print("\nIncident Briefing:\n", res["incident_briefing"])
