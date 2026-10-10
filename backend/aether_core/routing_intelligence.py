from __future__ import annotations

from typing import Any, Dict


ROLE_BY_DEPARTMENT = {
    "Revenue": "revenue_case_section",
    "Registration": "registration_case_section",
    "Municipal": "municipal_case_section",
    "Food Safety": "food_safety_case_section",
    "Labour": "labour_case_section",
    "Health": "health_regulatory_section",
    "Transport": "transport_case_section",
    "Tax": "tax_case_section",
    "Police": "police_case_section",
    "Education": "education_case_section",
    "Social Welfare": "welfare_case_section",
    "Environment": "environment_case_section",
    "Forest": "forest_case_section",
    "Mines": "mines_case_section",
    "Courts": "registry_or_court_section",
    "Passport": "passport_case_section",
}


def recommend_route(
    *,
    department: str,
    jurisdiction: Dict[str, Any],
    priority: str,
    human_boundary: bool = False,
    physical_action: bool = False,
    exception_count: int = 0,
) -> Dict[str, Any]:
    role = ROLE_BY_DEPARTMENT.get(department, "department_case_section")
    escalation = "standard"
    reasons = [f"service department={department}", f"priority={priority}"]

    if priority == "high":
        escalation = "priority_queue"
        reasons.append("case triage marked high priority")
    if exception_count:
        escalation = "exception_queue"
        reasons.append("case has unresolved exception(s)")
    if physical_action:
        reasons.append("field-work section required")
    if human_boundary:
        reasons.append("statutory authority is required")

    return {
        "department": department,
        "recommended_section": role,
        "jurisdiction": jurisdiction,
        "priority": priority,
        "escalation": escalation,
        "reasons": reasons,
        "auto_assignment": False,
        "assignment_connector_required": True,
        "safe_default": "prepare_and_route_for_authorised_assignment",
    }
