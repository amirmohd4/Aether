from __future__ import annotations

from datetime import datetime, timezone
import os
from typing import Any, Dict, List

from .notifications import NotificationService
from .payments import PaymentService
from .process_work_recipes import work_recipe, work_atom_metadata
from .journey_cascades import cascade_for
from .case_continuity import build_continuity_review
from backend.database import SessionLocal


class AdministrativeWorker:
    """Execute repetitive administrative work around a government case.

    This worker prepares or performs administrative operations only. It never
    makes a statutory decision, fabricates an inspection finding, or claims a
    record was changed unless a configured connector returned confirmation.
    """

    name = "AdministrativeWorker"

    def __init__(self, connectors=None):
        self.connectors = connectors

    def _external_action_enabled(self) -> bool:
        return os.getenv("AETHER_ENABLE_ADMIN_CONNECTOR_ACTIONS", "").strip().lower() == "true"

    def _execute_external(self, department: str, operation: str, payload: Dict[str, Any], idempotency_key: str | None) -> Dict[str, Any]:
        if not self._external_action_enabled() or not self.connectors:
            return {"status": "not_submitted", "reason": "admin connector execution is disabled"}
        if not self.connectors.is_production(department):
            return {"status": "not_submitted", "reason": "no authorised production connector configured"}
        result = self.connectors.get(department).execute(operation, payload, idempotency_key)
        return {
            "status": result.get("status", "unknown"),
            "request_id": result.get("request_id"),
            "result": result.get("result") or {},
            "source": result.get("source"),
        }

    def execute(self, context) -> Dict[str, Any]:
        operation = context.operation
        handlers = {
            "case_triage": self._triage,
            "case_file_assembly": self._file_assembly,
            "data_normalization": self._normalize,
            "assignment": self._assignment,
            "form_prep": self._form_prep,
            "case_notes": self._case_notes,
            "deficiency": self._deficiency,
            "query_response": self._query_response,
            "correspondence": self._correspondence,
            "followup_plan": self._followup,
            "sla_snapshot": self._sla_snapshot,
            "interim_response": self._interim_response,
            "recovery_plan": self._recovery_plan,
            "journey_cascade": self._journey_cascade,
            "continuity_review": self._continuity_review,
            "preflight_check": self._preflight_check,
            "interdepartment_handoff": self._interdepartment_handoff,
            "inspection_packet": self._inspection_packet,
            "joint_inspection": self._joint_inspection,
            "shared_compliance_profile": self._shared_compliance_profile,
            "renewal_bundle": self._renewal_bundle,
            "fee_reconciliation": self._fee_reconciliation,
            "decision_brief": self._decision_brief,
            "post_decision": self._post_decision,
            "case_closeout": self._closeout,
            "work_atom": self._work_atom,
        }
        handler = handlers.get(operation)
        if handler is None:
            return {
                "request_id": f"ADMIN-{context.case_id}-{operation}",
                "status": "completed",
                "result": {
                    "operation": operation,
                    "completed": True,
                    "source": "Aether Administrative Worker",
                },
            }
        return handler(context)

    @staticmethod
    def _result(context, operation: str, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "request_id": f"ADMIN-{context.case_id}-{operation.upper()}",
            "status": "completed",
            "result": {
                "operation": operation,
                **result,
                "source": "Aether Administrative Worker",
            },
        }

    @staticmethod
    def _preflight_check(context) -> Dict[str, Any]:
        payload = context.payload
        required = [str(x) for x in (payload.get("required_documents") or [])]
        submitted = {
            str(item.get("type")) if isinstance(item, dict) else str(item)
            for item in (payload.get("documents") or [])
        }
        missing = sorted(set(required) - submitted)
        normalized = ((payload.get("task_results") or {}).get("internal_data_normalization") or {}).get("normalized_fields") or {}
        continuity = ((payload.get("task_results") or {}).get("internal_continuity_review") or {})
        warnings = continuity.get("preflight_warnings") or []
        blocking = [
            {"type": "missing_document", "document_type": item}
            for item in missing
        ]
        blocking.extend(
            {"type": "recurring_issue", "code": item.get("code"), "occurrences": item.get("occurrences", 0)}
            for item in warnings
            if item.get("occurrences", 0) >= 2
        )
        return AdministrativeWorker._result(context, "preflight_check", {
            "ready_for_submission": not blocking,
            "blocking_items": blocking[:20],
            "warnings": warnings[:20],
            "normalized_field_count": len(normalized),
            "preventive_strategy": "resolve predictable issues before external submission instead of generating downstream rework",
        })

    @staticmethod
    def _continuity_review(context) -> Dict[str, Any]:
        payload = context.payload
        review = build_continuity_review(
            tenant_id=payload.get("tenant_id"),
            owner_user_id=payload.get("owner_user_id"),
            service_id=payload.get("service_id"),
            current_inputs=payload,
        )
        return AdministrativeWorker._result(context, "continuity_review", review)

    @staticmethod
    def _journey_cascade(context) -> Dict[str, Any]:
        service_id = str((context.payload or {}).get("service_id") or "")
        return AdministrativeWorker._result(context, "journey_cascade", {
            "source_service_id": service_id,
            "downstream_journey": cascade_for(service_id),
            "mode": "prepare",
        })

    def _work_atom(self, context) -> Dict[str, Any]:
        payload = context.payload
        atom = str(payload.get("work_atom") or "").strip()
        metadata = work_atom_metadata().get(atom, {
            "label": atom.replace("_", " ").title(),
            "automation": "prepare_only",
            "human_boundary": False,
        })
        automation = str(metadata.get("automation") or "prepare_only")
        external = {"status": "not_submitted", "reason": "prepare-only atom"}
        if automation in {"full_with_connector", "rule_backed"} and automation == "full_with_connector":
            external = self._execute_external(
                str(payload.get("service_department") or ""),
                atom,
                {
                    "case_id": context.case_id,
                    "service_id": payload.get("service_id"),
                    "objective": payload.get("objective"),
                    "jurisdiction": payload.get("jurisdiction") or {},
                    "task_results": payload.get("task_results") or {},
                },
                f"{context.case_id}:admin:atom:{atom}",
            )
        elif automation == "rule_backed":
            external = {
                "status": "prepared",
                "reason": "Requires authoritative effective-dated rule evaluation before external execution",
            }
        return AdministrativeWorker._result(context, "work_atom", {
            "work_atom": atom,
            "label": metadata.get("label"),
            "automation_mode": automation,
            "prepared": True,
            "connector_action": external,
            "authority_boundary": bool(metadata.get("human_boundary")),
        })

    @staticmethod
    def _triage(context) -> Dict[str, Any]:
        payload = context.payload
        objective = str(payload.get("objective") or "")
        customer_type = str(payload.get("customer_type") or "unknown")
        jurisdiction = payload.get("jurisdiction") or {}
        priority = "high" if any(
            token in objective.lower()
            for token in ("urgent", "deadline", "renewal", "inspection", "appeal", "hearing", "notice")
        ) else "normal"
        return AdministrativeWorker._result(context, "case_triage", {
            "priority": priority,
            "customer_type": customer_type,
            "jurisdiction": jurisdiction,
            "routing": {
                "department": payload.get("service_department") or "determine_from_service_profile",
                "case_owner": payload.get("owner_user_id"),
            },
            "risk_flags": list(payload.get("risk_flags") or []),
            "service_id": payload.get("service_id"),
            "process_profile": payload.get("process_profile", "generic"),
            "employee_work_recipe": work_recipe(payload.get("process_profile", "generic")),
        })

    @staticmethod
    def _file_assembly(context) -> Dict[str, Any]:
        payload = context.payload
        documents = payload.get("documents") or []
        required = payload.get("required_documents") or []
        submitted = {
            str(item.get("type")) if isinstance(item, dict) else str(item)
            for item in documents
        }
        checklist = [
            {
                "document_type": document,
                "status": "received" if document in submitted else "missing",
            }
            for document in required
        ]
        return AdministrativeWorker._result(context, "case_file_assembly", {
            "case_file_ready": not any(item["status"] == "missing" for item in checklist),
            "document_checklist": checklist,
            "received_documents": sorted(submitted),
            "missing_documents": [item["document_type"] for item in checklist if item["status"] == "missing"],
        })

    @staticmethod
    def _normalize(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        normalized: Dict[str, Any] = {}
        provenance: Dict[str, Dict[str, Any]] = {}

        for key in (
            "owner_name",
            "applicant_name",
            "company_name",
            "company_id",
            "property_id",
            "parcel_id",
            "project_id",
            "registration_id",
            "certificate_reference",
            "search_id",
            "record_reference",
            "tax_id",
            "gstin",
            "pan",
            "address",
        ):
            if payload.get(key) is not None:
                normalized[key] = payload[key]
                provenance[key] = {
                    "source": "case_input",
                    "field": key,
                }

        for task_id, result in results.items():
            if not isinstance(result, dict):
                continue
            inspection = result.get("document_inspection") or {}
            for check in inspection.get("checks", []):
                if not isinstance(check, dict):
                    continue
                for key, value in (check.get("extracted") or {}).items():
                    if value is not None and key not in normalized:
                        normalized[key] = value
                        provenance[key] = {
                            "source": f"document:{check.get('document_type', 'unknown')}",
                            "task": task_id,
                        }
            for key in (
                "registration_id",
                "certificate_reference",
                "search_id",
                "record_reference",
                "owner",
                "owner_name",
                "company_id",
                "property_id",
                "parcel_id",
                "project_id",
                "tax_id",
                "gstin",
                "pan",
                "address",
                "area",
            ):
                if result.get(key) is not None and key not in normalized:
                    normalized[key] = result[key]
                    provenance[key] = {
                        "source": f"task:{task_id}",
                        "field": key,
                    }

        return AdministrativeWorker._result(context, "data_normalization", {
            "normalized_fields": normalized,
            "field_provenance": provenance,
            "field_count": len(normalized),
        })

    def _assignment(self, context) -> Dict[str, Any]:
        payload = context.payload
        triage = (payload.get("task_results") or {}).get("internal_case_triage") or {}
        routing = triage.get("routing") or {}
        priority = triage.get("priority", "normal")
        service_department = payload.get("service_department") or routing.get("department") or "unassigned"
        current_owner = payload.get("owner_user_id")
        reason = [
            "jurisdiction matched to case",
            f"service department={service_department}",
            f"priority={priority}",
        ]
        if current_owner:
            reason.append("existing case owner retained")
        external = self._execute_external(
            str(service_department),
            "assign_case",
            {
                "case_id": context.case_id,
                "recommended_owner": current_owner,
                "priority": priority,
                "jurisdiction": payload.get("jurisdiction") or {},
            },
            f"{context.case_id}:admin:assign",
        )
        return AdministrativeWorker._result(context, "assignment", {
            "assignment_status": external.get("status") if external.get("status") != "not_submitted" else "recommended",
            "connector_response": external,
            "recommended_department": service_department,
            "recommended_owner": current_owner,
            "jurisdiction": payload.get("jurisdiction") or {},
            "priority": priority,
            "reason": reason,
            "workload_lookup": "requires department staffing connector",
        })

    def _form_prep(self, context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        normalized_result = results.get("internal_data_normalization") or {}
        fields = normalized_result.get("normalized_fields") or {}
        provenance = normalized_result.get("field_provenance") or {}
        target = payload.get("service_id") or payload.get("service_outcome") or "government_service"
        external = self._execute_external(
            str(payload.get("service_department") or ""),
            "prepare_form",
            {"case_id": context.case_id, "service_id": target, "fields": fields, "field_provenance": provenance},
            f"{context.case_id}:admin:prepare_form",
        )
        return AdministrativeWorker._result(context, "form_prep", {
            "target_service": target,
            "target_department": payload.get("service_department"),
            "form_status": "prepared_from_verified_case_facts",
            "fields": [
                {
                    "name": key,
                    "value": value,
                    "provenance": provenance.get(key),
                }
                for key, value in sorted(fields.items())
            ],
            "unmapped_required_fields": [],
            "connector_submission": external,
        })

    @staticmethod
    def _case_notes(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        task_states = payload.get("task_states") or {}
        exceptions = payload.get("case_exceptions") or []
        completed = [
            task_id for task_id, state in task_states.items()
            if isinstance(state, dict) and state.get("status") == "completed"
        ]
        queries = [
            task_id for task_id, result in results.items()
            if isinstance(result, dict) and result.get("status") in {"query", "needs_attention"}
        ]
        return AdministrativeWorker._result(context, "case_notes", {
            "case_summary": payload.get("objective"),
            "completed_task_count": len(completed),
            "source_task_ids": sorted(results.keys()),
            "open_exception_count": len(exceptions),
            "query_or_attention_tasks": sorted(queries),
            "chronology": [
                {
                    "task_id": task_id,
                    "status": state.get("status"),
                    "attempts": state.get("attempts", 0),
                    "started_at": state.get("started_at"),
                    "completed_at": state.get("completed_at"),
                }
                for task_id, state in sorted(task_states.items())
                if isinstance(state, dict)
            ],
            "next_official_action": (
                "Review highlighted exceptions/queries."
                if exceptions or queries
                else "Proceed with the next ready statutory or administrative step."
            ),
        })

    @staticmethod
    def _deficiency(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        documents = payload.get("documents") or []
        required = payload.get("required_documents") or []
        submitted = {
            str(item.get("type")) if isinstance(item, dict) else str(item)
            for item in documents
        }
        items: List[Dict[str, Any]] = [
            {
                "code": "MISSING_DOCUMENT",
                "document_type": doc,
                "severity": "high",
                "fix": f"Provide {doc}.",
                "applicant_fixable": True,
            }
            for doc in required
            if doc not in submitted
        ]

        for task_id, result in results.items():
            if not isinstance(result, dict):
                continue
            inspection = result.get("document_inspection") or {}
            for check in inspection.get("checks", []):
                if check.get("status") not in {None, "valid"}:
                    items.append({
                        "code": "DOCUMENT_CHECK_FAILURE",
                        "task_id": task_id,
                        "document_type": check.get("document_type"),
                        "severity": "high",
                        "issues": check.get("issues") or [],
                        "fix": "Review and replace the affected document.",
                        "applicant_fixable": True,
                    })
            findings = result.get("findings") or []
            for finding in findings:
                items.append({
                    "code": "SOURCE_FINDING",
                    "task_id": task_id,
                    "severity": finding.get("severity", "medium"),
                    "message": finding.get("message") or finding.get("code"),
                    "fix": "Resolve the finding or route it for authorised review.",
                    "applicant_fixable": False,
                })

        dedup: Dict[str, Dict[str, Any]] = {}
        for item in items:
            key = "|".join(str(item.get(x, "")) for x in ("code", "task_id", "document_type", "message"))
            dedup[key] = item
        return AdministrativeWorker._result(context, "deficiency", {
            "deficiency_count": len(dedup),
            "deficiencies": list(dedup.values()),
            "ready_for_complete_scrutiny": not dedup,
        })

    @staticmethod
    def _query_response(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        query_sources = []
        evidence = []
        for task_id, result in sorted(results.items()):
            if not isinstance(result, dict):
                continue
            if result.get("status") == "query" or result.get("query"):
                query_sources.append({
                    "task_id": task_id,
                    "query": result.get("query") or result.get("reason") or "Government query requires response.",
                    "reference": result.get("reference") or result.get("request_id"),
                })
            evidence.append({
                "task_id": task_id,
                "reference": (
                    result.get("reference")
                    or result.get("registration_id")
                    or result.get("certificate_reference")
                    or result.get("record_reference")
                ),
                "source": result.get("source"),
            })
        return AdministrativeWorker._result(context, "query_response", {
            "query_present": bool(query_sources),
            "queries": query_sources,
            "response_packet": (
                {
                    "case_id": context.case_id,
                    "facts_supported_by_evidence": evidence,
                    "response_draft": "Prepared from current case evidence; authorised review required before submission.",
                    "submission_status": "not_submitted",
                }
                if query_sources
                else None
            ),
            "authority_required": bool(query_sources),
        })

    def _correspondence(self, context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        deficiency = results.get("internal_deficiency") or {}
        missing = [
            item.get("document_type")
            for item in deficiency.get("deficiencies", [])
            if item.get("code") == "MISSING_DOCUMENT"
        ]
        query_results = [
            task_id for task_id, result in results.items()
            if isinstance(result, dict) and (
                result.get("status") == "query" or result.get("query")
            )
        ]

        drafts: List[Dict[str, Any]] = []
        if missing:
            drafts.append({
                "type": "missing_documents",
                "subject": "Additional documents required",
                "message": "Please provide: " + ", ".join(sorted(set(filter(None, missing)))),
            })
        if query_results:
            drafts.append({
                "type": "government_query",
                "subject": "Government query requires response",
                "message": "Review and respond to the query returned for: " + ", ".join(sorted(query_results)),
            })
        if not drafts:
            drafts.append({
                "type": "progress_update",
                "subject": "Case processing update",
                "message": "Aether has completed the current administrative processing stage.",
            })

        notification_ids = []
        service = NotificationService(SessionLocal)
        tenant_id = payload.get("tenant_id")
        user_id = payload.get("owner_user_id")
        for index, draft in enumerate(drafts):
            item = service.enqueue(
                tenant_id=tenant_id,
                user_id=user_id,
                case_id=context.case_id,
                event_type="case.correspondence.prepared",
                channel="in_app",
                payload=draft,
                idempotency_key=f"{context.case_id}:correspondence:{index}:{draft['type']}",
            )
            notification_ids.append(item["id"])

        return AdministrativeWorker._result(context, "correspondence", {
            "drafts": drafts,
            "notification_ids": notification_ids,
        })

    @staticmethod
    def _followup(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        pending: List[Dict[str, Any]] = []
        for task_id, result in results.items():
            if not isinstance(result, dict):
                continue
            if result.get("status") == "query" or result.get("needs_attention"):
                pending.append({
                    "task_id": task_id,
                    "action": "review_and_respond",
                    "reason": "source returned a query or attention condition",
                })

        deficiency = results.get("internal_deficiency") or {}
        for item in deficiency.get("deficiencies", []):
            pending.append({
                "action": "collect_evidence",
                "reason": item.get("fix"),
                "document_type": item.get("document_type"),
            })

        return AdministrativeWorker._result(context, "followup_plan", {
            "pending_followups": pending,
            "automatic_followup_enabled": True,
            "requires_replan_after_external_response": bool(pending),
        })

    @staticmethod
    @staticmethod
    def _interim_response(context) -> Dict[str, Any]:
        payload = context.payload
        states = payload.get("task_states") or {}
        results = payload.get("task_results") or {}
        missing = []
        for result in results.values():
            if isinstance(result, dict):
                missing.extend(result.get("deficiencies") or [])
        action_items = [
            {
                "type": item.get("code", "deficiency"),
                "document_type": item.get("document_type"),
                "message": item.get("fix") or item.get("message"),
            }
            for item in missing
            if item.get("applicant_fixable")
        ]
        pending = [
            str(task_id) for task_id, state in states.items()
            if isinstance(state, dict) and state.get("status") not in {"completed", "human_review"}
        ]
        return AdministrativeWorker._result(context, "interim_response", {
            "type": "action_required" if action_items else "interim_progress" if pending else "no_action",
            "customer_action_required": bool(action_items),
            "customer_actions": action_items[:20],
            "pending_task_ids": pending[:50],
            "message": (
                "Only the listed missing items need to be supplied."
                if action_items
                else "Aether is progressing the case and will resume the affected branch when its prerequisite is available."
                if pending
                else "No interim action is required."
            ),
            "no_restart_required": True,
        })

    @staticmethod
    def _recovery_plan(context) -> Dict[str, Any]:
        payload = context.payload
        states = payload.get("task_states") or {}
        exceptions = payload.get("case_exceptions") or []
        retry = []
        replan = []
        for task_id, state in states.items():
            if not isinstance(state, dict):
                continue
            status = state.get("status")
            error = str(state.get("error") or "").lower()
            if status == "exception":
                retry.append(task_id)
                if any(word in error for word in ("connector", "portal", "timeout", "http")):
                    replan.append(task_id)
            elif status == "blocked":
                replan.append(task_id)
        return AdministrativeWorker._result(context, "recovery_plan", {
            "recovery_required": bool(retry or replan or exceptions),
            "retry_tasks": sorted(set(retry)),
            "replan_tasks": sorted(set(replan)),
            "preserve_case_state": True,
            "preserve_verified_evidence": True,
            "ask_user_to_reenter_data": False,
            "compare_only_changed_inputs": True,
        })

    @staticmethod
    def _sla_snapshot(context) -> Dict[str, Any]:
        payload = context.payload
        states = payload.get("task_states") or {}
        now = datetime.now(timezone.utc)
        ageing: List[Dict[str, Any]] = []
        for task_id, state in states.items():
            if not isinstance(state, dict):
                continue
            if state.get("status") in {"completed", "human_review"}:
                continue
            started = state.get("started_at")
            if not started:
                continue
            try:
                dt = datetime.fromisoformat(str(started).replace("Z", "+00:00"))
                age_minutes = max(0, int((now - dt).total_seconds() / 60))
            except ValueError:
                continue
            if age_minutes >= 30:
                ageing.append({
                    "task_id": task_id,
                    "age_minutes": age_minutes,
                    "risk": "high" if age_minutes >= 120 else "medium",
                })
        return AdministrativeWorker._result(context, "sla_snapshot", {
            "ageing_tasks": ageing,
            "at_risk_count": len(ageing),
            "sla_policy_source": "service-specific authority/rule pack required",
            "escalation_status": "prepared_only",
        })

    def _interdepartment_handoff(self, context) -> Dict[str, Any]:
        payload = context.payload
        original_tasks = payload.get("original_tasks") or []
        departments: Dict[str, List[str]] = {}
        for task in original_tasks:
            if not isinstance(task, dict):
                continue
            department = str(task.get("department") or "").strip()
            if not department or department.lower() == "aether":
                continue
            departments.setdefault(department, []).append(str(task.get("id")))
        packets = []
        for department, task_ids in sorted(departments.items()):
            request_payload = {
                "case_id": context.case_id,
                "task_ids": task_ids,
                "request": "Provide the departmental evidence/report required by the case graph.",
            }
            external = self._execute_external(
                department,
                "interdepartment_request",
                request_payload,
                f"{context.case_id}:admin:interdepartment:{department}",
            )
            packets.append({
                "department": department,
                "task_ids": task_ids,
                "request": request_payload["request"],
                "due_date": None,
                "submission_status": external.get("status", "not_submitted"),
                "connector_response": external,
                "connector_required": True,
            })
        return AdministrativeWorker._result(context, "interdepartment_handoff", {
            "handoff_packets": packets,
            "department_count": len(packets),
        })

    @staticmethod
    def _joint_inspection(context) -> Dict[str, Any]:
        payload = context.payload
        physical_tasks = payload.get("physical_tasks") or []
        departments = sorted({
            str(task.get("department"))
            for task in physical_tasks
            if isinstance(task, dict) and task.get("department")
        })
        return AdministrativeWorker._result(context, "joint_inspection", {
            "candidate": len(physical_tasks) > 1,
            "physical_task_count": len(physical_tasks),
            "departments": departments,
            "shared_checklist": payload.get("inspection_checklist") or [],
            "strategy": "joint_or_coordinated_inspection_when_permitted",
            "risk_inputs": [
                "service risk classification",
                "prior compliance history",
                "complaint/enforcement history",
                "recent inspection evidence",
            ],
            "authority_required": True,
            "note": "Aether proposes coordination; an authorised authority decides inspection scope and findings.",
        })

    @staticmethod
    def _shared_compliance_profile(context) -> Dict[str, Any]:
        payload = context.payload
        normalized = (payload.get("task_results") or {}).get("internal_data_normalization") or {}
        fields = normalized.get("normalized_fields") or {}
        results = payload.get("task_results") or {}
        references = []
        for task_id, result in sorted(results.items()):
            if not isinstance(result, dict):
                continue
            ref = result.get("reference") or result.get("record_reference") or result.get("certificate_reference")
            if ref:
                references.append({"task_id": task_id, "reference": ref, "source": result.get("source")})
        return AdministrativeWorker._result(context, "shared_compliance_profile", {
            "profile_scope": "case_and_authorised_related_workflows",
            "consent_required_for_future_reuse": True,
            "verified_fields": fields,
            "evidence_references": references,
            "reuse_strategy": "reuse_verified_facts_and_changed_fields_only",
            "duplicate_submission_reduction": "prepare_once_share_by_authorised_connector",
        })

    @staticmethod
    def _renewal_bundle(context) -> Dict[str, Any]:
        payload = context.payload
        return AdministrativeWorker._result(context, "renewal_bundle", {
            "bundle_status": "prepared",
            "service_id": payload.get("service_id"),
            "renewal_strategy": "single_case_bundle_for_related_regulatory_renewals",
            "included_records": sorted((payload.get("task_results") or {}).keys()),
            "next_due_date_source": "authoritative_rule_profile_required",
            "auto_renewal": False,
            "authority_review_required": True,
            "customer_reentry_required": False,
        })

    @staticmethod
    def _inspection_packet(context) -> Dict[str, Any]:
        payload = context.payload
        physical_tasks = payload.get("physical_tasks") or []
        results = payload.get("task_results") or {}
        evidence = []
        for task_id, result in results.items():
            if isinstance(result, dict):
                evidence.append({
                    "task_id": task_id,
                    "reference": result.get("reference") or result.get("record_reference"),
                    "source": result.get("source", "Aether"),
                })
        packets = []
        for task in physical_tasks:
            packets.append({
                "task_id": task.get("id"),
                "task": task.get("name"),
                "department": task.get("department"),
                "checklist": task.get("inspection_checklist") or [],
                "authority_required": True,
                "result_status": "awaiting_authorised_inspection",
            })
        return AdministrativeWorker._result(context, "inspection_packet", {
            "packets": packets,
            "supporting_evidence": evidence,
            "inspection_finding_source": "authorised_officer_only",
        })

    @staticmethod
    def _fee_reconciliation(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        due_candidates = []
        for key in ("fee_due_minor", "demand_minor", "dues_minor", "amount_due_minor"):
            if payload.get(key) is not None:
                try:
                    due_candidates.append(int(payload[key]))
                except (TypeError, ValueError):
                    pass
        for result in results.values():
            if not isinstance(result, dict):
                continue
            for key in ("fee_due_minor", "demand_minor", "dues_minor", "amount_due_minor"):
                if result.get(key) is not None:
                    try:
                        due_candidates.append(int(result[key]))
                    except (TypeError, ValueError):
                        pass
        known_due = max(due_candidates) if due_candidates else None
        payments: List[Dict[str, Any]] = []
        tenant_id = payload.get("tenant_id")
        if tenant_id:
            try:
                payments = PaymentService(SessionLocal).for_case(tenant_id, context.case_id)
            except Exception:
                payments = []
        paid = sum(
            int(item.get("amount_minor") or 0)
            for item in payments
            if item.get("status") == "succeeded"
        )
        balance = None if known_due is None else max(0, known_due - paid)
        return AdministrativeWorker._result(context, "fee_reconciliation", {
            "known_demand_minor": known_due,
            "paid_minor": paid,
            "balance_minor": balance,
            "payment_records": payments,
            "reconciliation_status": (
                "balanced" if known_due is not None and balance == 0
                else "payment_due" if known_due is not None and balance > 0
                else "awaiting_authoritative_demand"
            ),
            "demand_source": "case_input_or_connector_result",
        })

    @staticmethod
    def _decision_brief(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        exceptions = payload.get("case_exceptions") or []
        evidence = []
        for task_id, result in sorted(results.items()):
            if not isinstance(result, dict):
                continue
            evidence.append({
                "task_id": task_id,
                "verified": result.get("verified", result.get("validated", True)),
                "reference": result.get("reference")
                    or result.get("registration_id")
                    or result.get("certificate_reference")
                    or result.get("record_reference"),
                "source": result.get("source"),
            })
        return AdministrativeWorker._result(context, "decision_brief", {
            "decision_status": "prepared_for_authorised_decision",
            "issue": payload.get("objective"),
            "service_id": payload.get("service_id"),
            "service_outcome": payload.get("service_outcome"),
            "evidence": evidence,
            "exceptions": exceptions,
            "rule_references": [],
            "recommendation": None,
            "decision": None,
            "authority_required": True,
        })

    def _post_decision(self, context) -> Dict[str, Any]:
        payload = context.payload
        states = payload.get("task_states") or {}
        non_admin = [
            state for state in states.values()
            if isinstance(state, dict) and state.get("department", "").lower() != "aether"
        ]
        service_complete = bool(non_admin) and all(
            state.get("status") == "completed"
            for state in non_admin
        )
        results = payload.get("task_results") or {}
        actions = [
            "prepare final outcome/certificate/order packet",
            "update authoritative record through configured connector",
            "dispatch applicant notification",
            "start renewal/compliance watch where applicable",
            "prepare audit/retention packet",
        ]
        external = self._execute_external(
            str(payload.get("service_department") or ""),
            "post_decision_update",
            {
                "case_id": context.case_id,
                "service_id": payload.get("service_id"),
                "service_outcome": payload.get("service_outcome"),
                "task_results": results,
            },
            f"{context.case_id}:admin:post_decision_update",
        )
        return AdministrativeWorker._result(context, "post_decision", {
            "ready_for_post_decision": service_complete,
            "actions": actions,
            "connector_action": external,
            "record_update_status": external.get("status", "not_submitted"),
            "notification_status": "not_dispatched",
            "renewal_status": "to_schedule_from_authoritative_rules",
        })

    @staticmethod
    def _closeout(context) -> Dict[str, Any]:
        results = context.payload.get("task_results") or {}
        references = []
        for task_id, result in results.items():
            if isinstance(result, dict):
                ref = (
                    result.get("reference")
                    or result.get("certificate_reference")
                    or result.get("record_reference")
                    or result.get("registration_id")
                )
                if ref:
                    references.append({"task_id": task_id, "reference": ref})
        states = context.payload.get("task_states") or {}
        all_complete = bool(states) and all(
            isinstance(state, dict) and state.get("status") == "completed"
            for state in states.values()
        )
        return AdministrativeWorker._result(context, "case_closeout", {
            "case_file_references": references,
            "administrative_closeout_complete": all_complete,
            "ready_to_archive": all_complete,
        })
