"""Autonomous Incident Severity Assessor and Escalation Matrix Coordinator.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class IncidentSeverityCoordinator:
    """Evaluates IT service outages and customer impact signals to assign standardized
    incident severity (SEV0 to SEV3), trigger on-call paging hierarchies, and draft incident briefings."""

    SEVERITY_LEVELS = {
        "SEV0": {
            "title": "Catastrophic Global Outage",
            "sla_response_minutes": 5,
            "escalation_target": "Executive Crisis Team & VP Engineering",
            "paging_frequency_minutes": 5,
        },
        "SEV1": {
            "title": "Critical Core Flow Impairment",
            "sla_response_minutes": 15,
            "escalation_target": "Primary & Secondary Service On-Call Leads",
            "paging_frequency_minutes": 10,
        },
        "SEV2": {
            "title": "Major Feature Degradation / Workaround Available",
            "sla_response_minutes": 60,
            "escalation_target": "Service Primary On-Call",
            "paging_frequency_minutes": 30,
        },
        "SEV3": {
            "title": "Minor Non-Customer-Facing Glitch",
            "sla_response_minutes": 240,
            "escalation_target": "Next Business Day Queue",
            "paging_frequency_minutes": 0,
        },
    }

    @classmethod
    def assess_incident(
        cls,
        impact_metrics: Dict[str, Any],
        incident_description: str,
    ) -> Dict[str, Any]:
        """Calculates standardized severity based on revenue loss, affected user percentage, and core flow down."""
        user_impact_pct = float(impact_metrics.get("affected_users_percentage", 0.0))
        is_checkout_or_login = bool(impact_metrics.get("core_revenue_flow_down", False))
        data_loss_risk = bool(impact_metrics.get("data_loss_or_corruption", False))
        customer_facing = bool(impact_metrics.get("customer_facing", True))

        # Severity decision logic
        if (user_impact_pct >= 50.0 and is_checkout_or_login) or data_loss_risk:
            severity = "SEV0"
        elif user_impact_pct >= 10.0 or is_checkout_or_login:
            severity = "SEV1"
        elif user_impact_pct >= 1.0 and customer_facing:
            severity = "SEV2"
        else:
            severity = "SEV3"

        spec = cls.SEVERITY_LEVELS[severity]

        briefing = (
            f"[{severity} INCIDENT ALERT] {spec['title']}\n"
            f"Description: {incident_description}\n"
            f"Impact: {user_impact_pct}% users affected. Core Revenue Flow Down: {is_checkout_or_login}.\n"
            f"Response SLA: Under {spec['sla_response_minutes']} minutes. Target: {spec['escalation_target']}."
        )

        return {
            "assigned_severity": severity,
            "severity_title": spec["title"],
            "sla_response_minutes": spec["sla_response_minutes"],
            "escalation_target": spec["escalation_target"],
            "paging_frequency_minutes": spec["paging_frequency_minutes"],
            "incident_briefing": briefing,
            "requires_status_page_banner": severity in ["SEV0", "SEV1"],
        }
