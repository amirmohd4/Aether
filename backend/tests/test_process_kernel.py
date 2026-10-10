from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus
from aether_core.government_process_kernel import infer_process_profile


def test_process_kernel_assigns_deep_employee_work():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": [
            "identity_document",
            "lease_or_ownership",
            "business_registration",
        ]},
    )

    expected = {
        "internal_assignment",
        "internal_form_prep",
        "internal_case_notes",
        "internal_deficiency",
        "internal_sla_snapshot",
        "internal_decision_brief",
        "internal_post_decision",
        "internal_case_closeout",
    }
    assert expected.issubset(case.tasks.keys())
    assert infer_process_profile(engine.services.get("food_business_license")).key == "food_license"


def test_deep_employee_work_executes_before_statutory_boundary():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to build a commercial project",
        customer_type="developer",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": [
            "identity_document",
            "business_registration",
            "site_plan",
            "building_plan",
        ]},
    )
    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["internal_assignment"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_form_prep"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_case_notes"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_deficiency"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_decision_brief"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_inspection_packet"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_post_decision"].status != TaskStatus.COMPLETED


def test_india_service_family_catalog_expanded():
    engine = AetherExecutionEngine()
    catalog = engine.services.catalog()

    assert len(catalog) >= 100
    ids = {item["id"] for item in catalog}
    assert {"gst_return_filing", "property_tax_payment", "fire_noc", "old_age_pension", "rtI_application"}.issubset(ids)

    assert engine.services.resolve("I need a property tax receipt", "citizen").id == "property_tax_payment"
    assert engine.services.resolve("I need a fire NOC for my building", "business").id == "fire_noc"


def test_process_kernel_falls_back_by_department_for_new_family():
    engine = AetherExecutionEngine()
    service = engine.services.get("property_tax_payment")
    profile = infer_process_profile(service)

    assert profile.key == "municipal_license"
    assert profile.payment_sensitive is True


def test_external_service_catalog_loader_json(tmp_path):
    from aether_core.service_catalog_loader import load_records

    path = tmp_path / "services.json"
    path.write_text(
        '{"services":[{"id":"example_service","name":"Example Service","department":"Revenue","customer_types":["citizen"],"keywords":["example"]}]}',
        encoding="utf-8",
    )
    rows = load_records(path)

    assert rows[0][0] == "example_service"
    assert rows[0][1] == "Example Service"
    assert rows[0][3] == ["citizen"]


def test_jurisdiction_process_profile_registry_selects_most_specific_profile(tmp_path, monkeypatch):
    from aether_core.jurisdiction_process_profiles import JurisdictionProcessRegistry

    path = tmp_path / "profiles.json"
    path.write_text(
        '{"profiles":['
        '{"service_id":"fire_noc","country":"India","source_url":"https://example.gov","effective_date":"2026-01-01","verified_at":"2026-10-01","steps":[{"id":"scrutiny"}]},'
        '{"service_id":"fire_noc","country":"India","state":"Jammu and Kashmir","source_url":"https://jk.example.gov","effective_date":"2026-01-01","verified_at":"2026-10-01","steps":[{"id":"inspection"}]}'
        ']}',
        encoding="utf-8",
    )
    monkeypatch.setenv("AETHER_PROCESS_PROFILE_PATH", str(path))
    registry = JurisdictionProcessRegistry()

    profile = registry.resolve(
        "fire_noc",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
    )
    assert profile is not None
    assert profile.state == "Jammu and Kashmir"
    assert registry.readiness(
        "fire_noc",
        {"country": "India", "state": "Jammu and Kashmir"},
    )["status"] == "ready"


def test_dynamic_employee_work_atom_is_materialized_for_recipe_gap():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a property",
        customer_type="citizen",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document", "property_record"]},
    )
    assert "internal_work_atom_scrutinize_deed" in case.tasks or "internal_work_atom_prepare_registration_packet" in case.tasks


def test_production_connector_rejects_unauthorised_employee_operation():
    from aether_core.connectors import ConfiguredHTTPConnector

    connector = ConfiguredHTTPConnector(
        department="Municipal",
        base_url="https://example.gov",
        bearer_token="secret",
        allowed_operations={"assign_case"},
    )
    try:
        connector.submit("delete_record", {"case_id": "A-TEST"})
    except RuntimeError as exc:
        assert "not authorised" in str(exc)
    else:
        raise AssertionError("unauthorised connector operation must be rejected")


def test_case_exposes_recovery_and_interim_response_nodes():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a company",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document", "business_registration"]},
    )
    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["internal_interim_response"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_recovery_plan"].status == TaskStatus.COMPLETED
    operator = __import__("aether_core.employee_automation", fromlist=["EmployeeAutomationService"]).EmployeeAutomationService().brief(case)
    assert "friction" in operator
    assert operator["friction"]["recovery_plan"]["ask_user_to_reenter_data"] is False


def test_regulated_case_prepares_shared_compliance_and_joint_inspection():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={
            "documents": ["identity_document", "lease_or_ownership", "floor_plan"],
            "inspection_checklist": ["premises", "fire safety", "sanitation"],
        },
    )
    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["internal_shared_compliance_profile"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_joint_inspection"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_interim_response"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_recovery_plan"].status == TaskStatus.COMPLETED


def test_property_registration_prepares_downstream_journey():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a property",
        customer_type="citizen",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document", "property_record"]},
    )
    case = engine.execute_until_pause(case.case_id)
    result = case.tasks["internal_journey_cascade"].result or {}
    result = result.get("result") if isinstance(result, dict) and "result" in result else result
    downstream = result.get("downstream_journey") or []
    ids = {item["service_id"] for item in downstream}
    assert "mutation" in ids


def test_operator_batching_groups_repeated_automated_work():
    from aether_core.work_batching import build_operator_batches

    batches = build_operator_batches([
        {
            "case_id": "A-1",
            "next_best_actions": [
                {"type": "automated", "task_id": "internal_form_prep", "owner": "Aether"}
            ],
        },
        {
            "case_id": "A-2",
            "next_best_actions": [
                {"type": "automated", "task_id": "internal_form_prep", "owner": "Aether"}
            ],
        },
        {
            "case_id": "A-3",
            "next_best_actions": [
                {"type": "human", "task_id": "inspection", "owner": "Municipal"}
            ],
        },
    ])

    assert len(batches) == 1
    assert batches[0]["case_count"] == 2
    assert batches[0]["task_id"] == "internal_form_prep"
    assert batches[0]["execution_mode"] == "prepare_and_review"


def test_continuity_review_is_scoped_and_never_auto_reuses():
    from aether_core.case_continuity import build_continuity_review

    review = build_continuity_review(
        tenant_id=None,
        owner_user_id=None,
        service_id="company_registration",
    )
    assert review["status"] == "unavailable"
    assert review["policy"]["auto_copy"] is False
    assert review["policy"]["explicit_user_confirmation_required"] is True


def test_pension_case_preflight_is_materialized_and_completed():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to process a government pension claim",
        customer_type="citizen",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"employee_id": "EMP-1", "date_of_retirement": "2027-03-31"},
    )
    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["internal_retirement_preflight"].status == TaskStatus.COMPLETED
    result = case.tasks["internal_retirement_preflight"].result or {}
    assert result.get("status") in {"prepared", "completed"}


def test_case_passport_has_integrity_without_moving_documents():
    from aether_core.case_passport import build_case_passport

    passport = build_case_passport(
        case_id="A-TEST",
        service_id="company_registration",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        task_results={
            "registration": {
                "registration_id": "REG-1",
                "source": "Authorised Registry",
            }
        },
        verified_fields={"company_name": "Example Pvt Ltd"},
    )
    assert passport["documents_included"] is False
    assert passport["integrity"]["sha256"]
    assert passport["evidence_references"][0]["reference"] == "REG-1"


def test_grievance_case_has_whole_government_routing_step():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to file a government grievance",
        customer_type="citizen",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    assert "internal_whole_government_route" in case.tasks


def test_udyam_recipe_uses_authoritative_prefill():
    engine = AetherExecutionEngine()
    service = engine.services.get("udyam_registration")
    profile = infer_process_profile(service)
    assert profile.key == "msme_registration"
    assert "authoritative_prefill" in __import__(
        "aether_core.process_work_recipes",
        fromlist=["work_recipe"],
    ).work_recipe(profile.key)


def test_process_specific_work_patterns_are_bound():
    from aether_core.process_work_recipes import work_recipe

    assert "resubmission_diff_packet" in work_recipe("corporate_incorporation")
    assert "verification_chain_tracking" in work_recipe("passport")
    assert "service_center_packet" in work_recipe("customs")
    assert "intermediate_handoff_tracking" in work_recipe("police")


def test_workload_snapshot_groups_department_bottlenecks():
    from aether_core.workload_intelligence import build_workload_snapshot
    from aether_core.domain import Case, TaskDefinition, TaskState, TaskStatus

    case = Case(
        case_id="A-1",
        objective="test",
        customer_type="business",
        jurisdiction={"country": "India"},
        inputs={},
        requirements=[],
        tasks={
            "t1": TaskState(TaskDefinition("t1", "Review", "Municipal", "AdministrativeWorker"), status=TaskStatus.PENDING),
            "t2": TaskState(TaskDefinition("t2", "Review", "Municipal", "AdministrativeWorker"), status=TaskStatus.EXCEPTION),
        },
    )
    snapshot = build_workload_snapshot([case])
    municipal = next(item for item in snapshot["departments"] if item["department"] == "Municipal")
    assert municipal["pending"] == 1
    assert municipal["exceptions"] == 1
    assert municipal["management_attention"] == "high"


def test_employee_work_atoms_are_not_serialized_unnecessarily():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={},
    )
    file_deps = set(case.tasks["internal_case_file"].definition.dependencies)
    assert set(case.tasks["internal_authoritative_prefill"].definition.dependencies) == {"internal_case_file"}
    assert set(case.tasks["internal_continuity_review"].definition.dependencies) == {"internal_case_file"}
    assert case.tasks["internal_authoritative_prefill"].definition.dependencies != case.tasks["internal_data_normalization"].definition.dependencies
    assert "internal_case_triage" in file_deps


def test_health_claim_process_recipe_is_deep():
    from aether_core.process_work_recipes import work_recipe

    recipe = work_recipe("health_claim")
    assert "claim_query_tracking" in recipe
    assert "nodal_route" in recipe
    assert "claim_anomaly_screen" in recipe


def test_replan_resets_only_changed_branch_and_preserves_unrelated_completed_work():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={
            "documents": [
                "identity_document",
                "lease_or_ownership",
                "floor_plan",
                "business_registration",
            ]
        },
    )
    case = engine.execute_until_pause(case.case_id)

    unrelated = case.tasks.get("internal_case_triage")
    assert unrelated is not None
    assert unrelated.status == TaskStatus.COMPLETED

    replanned = engine.replan_case(
        case.case_id,
        ["document_intake"],
        reason="Applicant corrected a document.",
    )
    assert replanned.tasks["document_intake"].status in {
        TaskStatus.HUMAN_REVIEW,
        TaskStatus.COMPLETED,
        TaskStatus.EXCEPTION,
    }
    assert replanned.tasks["internal_case_triage"].status == TaskStatus.COMPLETED
    assert any(
        event.get("action") == "case.replanned"
        for event in replanned.execution_events
    )


def test_process_profile_change_status_detects_changed_authoritative_profile():
    from aether_core.jurisdiction_process_profiles import JurisdictionProcessProfile
    from aether_core.engine import AetherExecutionEngine

    engine = AetherExecutionEngine()
    profile = JurisdictionProcessProfile(
        service_id="fire_noc",
        country="India",
        state="Jammu and Kashmir",
        source_url="https://example.gov",
        effective_date="2026-01-01",
        verified_at="2026-10-01",
        steps=[{"id": "scrutiny"}],
        required_documents=["identity_document"],
        service_level={"days": 7},
    )
    engine.process_profiles.add(profile)

    case = engine.create_case(
        objective="I want a fire NOC for my building",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document"]},
    )

    changed = JurisdictionProcessProfile(
        service_id="fire_noc",
        country="India",
        state="Jammu and Kashmir",
        source_url="https://example.gov",
        effective_date="2026-02-01",
        verified_at="2026-10-10",
        steps=[{"id": "scrutiny"}, {"id": "inspection"}],
        required_documents=["identity_document", "site_plan"],
        service_level={"days": 5},
    )

    engine.process_profiles.add(changed)
    status = engine.process_profile_status(case)
    assert status["status"] == "changed"
    assert status["impact"]["impact"]["reprepare_forms"] is True


def test_inspection_quality_guard_requires_structured_packet():
    from aether_core.administrative_worker import AdministrativeWorker
    from aether_core.workers import WorkerContext

    result = AdministrativeWorker().execute(WorkerContext(
        case_id="A-TEST",
        department="Aether",
        operation="inspection_quality_guard",
        payload={
            "physical_tasks": [{"id": "inspection"}],
            "documents": [],
            "inspection_checklist": [],
        },
    ))
    assert result["status"] == "completed"
    assert result["result"]["ready_for_authorised_inspection"] is False
    codes = {item["code"] for item in result["result"]["blockers"]}
    assert {"NO_INSPECTION_CHECKLIST", "NO_SUPPORTING_EVIDENCE"}.issubset(codes)


def test_query_normalizer_turns_vague_query_into_action():
    from aether_core.query_normalizer import normalize_query

    result = normalize_query(
        "Please upload missing supporting document for GST registration",
        reference="Q-1",
        task_id="gst",
    )
    assert result["code"] == "MISSING_DOCUMENT"
    assert result["applicant_fixable"] is True
    assert result["task_id"] == "gst"


def test_submission_dry_run_stops_before_external_submission():
    from aether_core.preflight_simulator import simulate_submission

    result = simulate_submission(
        service=type("Service", (), {"id": "company_registration"})(),
        requirements=[{"documents": ["identity_document", "company_certificate"]}],
        inputs={"documents": ["identity_document"]},
        process_profile={"status": "ready"},
        journey_playbook={"stages": ["submission", "review"], "human_boundary": ["approval"]},
    )
    assert result["status"] == "fix_before_submit"
    assert result["policy"]["no_external_submission_performed"] is True
    assert result["blockers"][0]["code"] == "MISSING_DOCUMENT"


def test_form_mapper_eliminates_manual_copy_paste_and_tracks_provenance():
    from aether_core.field_mapper import prepare_form_mapping

    result = prepare_form_mapping(
        {"company_name": "Example Pvt Ltd", "pan": "ABCDE1234F"},
        {
            "company_name": {"source": "document:incorporation", "field": "company_name"},
            "pan": {"source": "connector:PAN", "field": "pan"},
        },
        required_fields=["company_name", "pan"],
    )
    assert result["mapping_status"] == "ready"
    assert result["copy_paste_eliminated"] is True
    assert {item["target_field"] for item in result["mapped_fields"]} == {"companyName", "pan"}


def test_duplicate_case_screen_flags_existing_case_without_auto_merge():
    from aether_core.duplicate_case_detection import find_duplicate_cases
    from aether_core.domain import Case

    class Store:
        def list(self, **kwargs):
            return [{"case_id": "A-OLD", "service_id": "property_registration"}]
        def get(self, case_id):
            return Case(
                case_id=case_id,
                objective="I want to register a property",
                customer_type="citizen",
                jurisdiction={"country": "India"},
                inputs={"property_id": "PROP-1"},
                requirements=[],
                tasks={},
                owner_user_id="U-1",
                tenant_id="T-1",
                service_id="property_registration",
            )

    case = Case(
        case_id="A-NEW",
        objective="I want to register a property",
        customer_type="citizen",
        jurisdiction={"country": "India"},
        inputs={"property_id": "PROP-1"},
        requirements=[],
        tasks={},
        owner_user_id="U-1",
        tenant_id="T-1",
        service_id="property_registration",
    )
    result = find_duplicate_cases(Store(), case)
    assert result["duplicate_candidate_count"] == 1
    assert result["auto_merge"] is False
    assert result["duplicate_candidates"][0]["confidence"] == "medium"


def test_remediation_planner_produces_one_clear_next_action():
    from aether_core.remediation_planner import build_remediation_plan

    result = build_remediation_plan(
        deficiencies=[{
            "code": "MISSING_DOCUMENT",
            "document_type": "site_plan",
            "fix": "Provide site plan",
            "applicant_fixable": True,
        }],
        queries=[{
            "code": "IDENTITY_MISMATCH",
            "recommended_action": "Correct the identity field",
            "applicant_fixable": True,
        }],
    )
    assert result["status"] == "action_required"
    assert result["actions"][0]["owner"] == "applicant"
    assert result["actions"][0]["blocks_case"] is True
