from backend.aether_core.employee_automation import EmployeeAutomationService
from backend.aether_core.domain import Case, TaskDefinition, TaskState, TaskStatus


def make_case() -> Case:
    tasks = {
        "document_intake": TaskState(
            TaskDefinition(
                "document_intake",
                "Validate documents",
                "Aether",
                "DocumentWorker",
            ),
            status=TaskStatus.COMPLETED,
        ),
        "reconciliation": TaskState(
            TaskDefinition(
                "reconciliation",
                "Reconcile records",
                "Aether",
                "ReconciliationWorker",
                ["document_intake"],
            ),
            status=TaskStatus.COMPLETED,
        ),
        "final_approval": TaskState(
            TaskDefinition(
                "final_approval",
                "Statutory approval",
                "Authorised Officer",
                "HumanAuthorityWorker",
                ["reconciliation"],
                authority_required=True,
            ),
            status=TaskStatus.HUMAN_REVIEW,
        ),
    }
    return Case(
        case_id="A-TEST123",
        objective="Approve a project",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document"]},
        requirements=[{"id": "x", "name": "x", "documents": ["identity_document", "site_plan"]}],
        tasks=tasks,
        service_id="building_permit",
        service_name="Building Permit",
        service_department="Municipal",
        service_outcome="building permit",
    )


def test_brief_separates_automation_from_human_boundary():
    brief = EmployeeAutomationService().brief(make_case())

    assert brief["summary"]["automated_completed"] == 2
    assert brief["summary"]["human_or_physical_total"] == 1
    assert brief["summary"]["employee_attention_required"] == 1
    assert brief["time"]["estimated_minutes_saved"] > 0
    assert brief["customer_actions"] == [
        {
            "type": "missing_document",
            "document": "site_plan",
            "action": "Upload this document to continue",
        }
    ]
    assert any(
        item["type"] == "human" and item["task_id"] == "final_approval"
        for item in brief["next_best_actions"]
    )


def test_brief_flags_outstanding_dues_without_deciding_statutory_outcome():
    case = make_case()
    case.tasks["reconciliation"].result = {
        "dues": 1250,
        "source": "Synthetic Tax Record",
    }

    brief = EmployeeAutomationService().brief(case)

    assert brief["revenue_signals"][0]["type"] == "outstanding_dues"
    assert "Reconcile dues" in brief["revenue_signals"][0]["action"]
