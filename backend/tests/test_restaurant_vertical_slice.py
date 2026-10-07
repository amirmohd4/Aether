from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


def test_restaurant_vertical_slice_reaches_human_boundary_then_completes():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        "I want to open a restaurant",
        "business",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {"documents": ["identity_document", "lease_or_ownership", "floor_plan"]},
    )

    paused = engine.execute_until_pause(case.case_id)
    assert paused.status == "waiting_for_human"
    human_ids = [a["task_id"] for a in paused.human_actions]
    assert "inspection" in human_ids

    resumed = engine.complete_human_task(case.case_id, "inspection", "approved", "Inspection passed")
    assert resumed.status == "waiting_for_human"
    assert any(a["task_id"] == "final_approval" for a in resumed.human_actions)

    completed = engine.complete_human_task(case.case_id, "final_approval", "approved", "Final statutory approval")
    assert completed.status == "completed"
    assert completed.outcome["status"] == "completed"
    assert all(task.status == TaskStatus.COMPLETED for task in completed.tasks.values())
