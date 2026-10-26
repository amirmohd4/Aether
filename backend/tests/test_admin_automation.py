from backend.aether_core.admin_automation import plan_administrative_actions


def test_plans_missing_evidence_action_with_stable_id():
    finding = {
        "code": "payment_claim_evidence_incomplete",
        "title": "Payment claim lacks evidence",
        "evidence_needed": ["invoice", "acceptance_record"],
    }
    first = plan_administrative_actions("CASE-1", [finding], [])
    second = plan_administrative_actions("CASE-1", [finding], [])
    assert first == second
    assert first["count"] == 1
    action = first["actions"][0]
    assert action["execution_mode"] == "proposed_not_enqueued"
    assert action["requires_human_decision"] is True


def test_deduplicates_same_finding_and_proposes_blocked_handoff():
    finding = {"code": "budget_unknown", "title": "Budget missing"}
    handoff = {"task_id": "approval", "task": "Approval", "department": "planning", "blocked_by": ["survey"]}
    result = plan_administrative_actions("CASE-1", [finding, finding], [handoff])
    assert result["count"] == 2
    assert {item["action_type"] for item in result["actions"]} == {
        "collect_approved_budget", "resolve_cross_department_handoff"
    }
