from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
import hashlib
import secrets

from .api_models import DocumentSubmissionRequest, HumanDecisionRequest, StartCaseRequest
from .engine import engine
from .requirements_engine import RequirementEngine
from .rule_registry import RuleRegistry
from .verification import VerificationEngine
from .security import Principal, require_principal, require_role, require_scope
from .understanding import ObjectiveUnderstandingEngine
from .document_store import DocumentStore, document_summary
from .notifications import NotificationService
from .payments import PaymentService
from .analytics import summarize_cases
from backend.database import SessionLocal
from sqlalchemy import text

router = APIRouter(prefix="/api/aether/v2", tags=["Aether V2"], dependencies=[Depends(require_principal)])
requirements_engine = RequirementEngine()
understanding_engine = ObjectiveUnderstandingEngine()
rule_registry = RuleRegistry()
verification_engine = VerificationEngine()
document_store = DocumentStore()
notification_service = NotificationService(SessionLocal)
payment_service = PaymentService(SessionLocal)


def serialize(case, include_tasks: bool = True):
    understanding = understanding_engine.understand(
        case.objective,
        case.customer_type,
        case.jurisdiction,
    )
    response = {
        "summary": case.summary(),
        "understanding": understanding.as_dict(),
        "requirements": case.requirements,
        "human_actions": case.human_actions,
        "exceptions": case.exceptions,
        "evidence": case.evidence,
        "outcome": case.outcome,
        "documents": engine.store.documents_for(case.case_id, case.tenant_id),
        "verification": verification_engine.reconcile({
            task_id: task.result
            for task_id, task in case.tasks.items()
            if task.result
        }).as_dict(),
        "queue": engine.queue.for_case(case.case_id),
        "execution_events": case.execution_events[-50:],
    }
    if include_tasks:
        response["tasks"] = {
            task_id: {
                "name": state.definition.name,
                "department": state.definition.department,
                "worker": state.definition.worker,
                "dependencies": state.definition.dependencies,
                "status": state.status.value,
                "authority_required": state.definition.authority_required,
                "physical_action": state.definition.physical_action,
                "result": state.result,
                "error": state.error,
                "evidence": state.evidence,
                "attempts": state.attempts,
                "idempotency_key": state.idempotency_key,
            }
            for task_id, state in case.tasks.items()
        }
    return response


@router.get("/release/readiness")
def release_readiness():
    import os
    production = os.getenv("AETHER_ENV", "development").strip().lower() == "production"
    checks = {
        "database_url": bool(os.getenv("DATABASE_URL")),
        "supabase_auth": os.getenv("AETHER_AUTH_MODE", "none").strip().lower() == "supabase",
        "encryption_key": bool(os.getenv("AETHER_ENCRYPTION_KEY")),
        "private_document_storage": bool(
            os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        ),
        "production_connectors": engine.workers.production_connectors_configured(),
        "authoritative_rule_coverage": len(rule_registry.all()) > 0,
        "legacy_api_quarantined": os.getenv("AETHER_ENABLE_LEGACY_API", "true").strip().lower() == "false",
        "synthetic_mode": not engine.workers.production_connectors_configured(),
    }
    blockers = []
    if production and not checks["database_url"]:
        blockers.append("DATABASE_URL is not configured")
    if production and not checks["supabase_auth"]:
        blockers.append("AETHER_AUTH_MODE must be supabase")
    if production and not checks["encryption_key"]:
        blockers.append("AETHER_ENCRYPTION_KEY is not configured")
    if production and not checks["private_document_storage"]:
        blockers.append("Private Supabase document storage is not configured")
    if production and not checks["production_connectors"]:
        blockers.append("No live government connectors are configured")
    if production and not checks["authoritative_rule_coverage"]:
        blockers.append("No authoritative rule records are configured")

    return {
        "mode": "production" if production else "development_or_staging",
        "ready_for_controlled_mvp": True,
        "ready_for_production": production and not blockers,
        "checks": checks,
        "blockers": blockers,
        "note": "Controlled MVP can run against deterministic synthetic government systems. Production readiness requires authorized live connectors and authoritative rule coverage."
    }


@router.get("/connectors")
def connector_catalog():
    return {
        "connectors": engine.workers.connector_catalog(),
        "default_mode": "synthetic",
        "production_connectors_configured": engine.workers.production_connectors_configured(),
    }


@router.get("/analytics")
def case_analytics(principal: Principal = Depends(require_scope("analytics:read"))):
    cases = (
        _list_visible_cases(principal, limit=100)
        if principal.auth_mode == "none"
        or principal.role.lower() in {"admin", "officer", "department_admin"}
        else engine.store.list(owner_user_id=principal.subject, limit=100)
    )
    return summarize_cases(cases)


@router.get("/notifications")
def notifications(principal: Principal = Depends(require_scope("cases:read"))):
    if not principal.tenant_id:
        raise HTTPException(status_code=403, detail="Active tenant is required")
    return {"notifications": notification_service.list_for_tenant(principal.tenant_id)}


@router.get("/cases/{case_id}/payments")
def case_payments(case_id: str, principal: Principal = Depends(require_scope("payments:read"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return {"payments": payment_service.for_case(principal.tenant_id or case.tenant_id or principal.subject, case_id)}
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/payments")
def create_case_payment(
    case_id: str,
    amount_minor: int,
    currency: str = "INR",
    idempotency_key: str | None = None,
    principal: Principal = Depends(require_scope("payments:write")),
):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        tenant_id = principal.tenant_id or case.tenant_id or principal.subject
        payment = payment_service.create(
            tenant_id,
            case_id,
            amount_minor,
            currency,
            idempotency_key,
            {"service_id": case.service_id, "service_outcome": case.service_outcome},
        )
        notification_service.enqueue(
            tenant_id,
            principal.subject,
            case_id,
            "payment.created",
            "in_app",
            payload={"payment_id": payment["payment_id"], "status": payment["status"]},
        )
        return payment
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/cases/{case_id}/intake")
def case_intake(case_id: str, principal: Principal = Depends(require_scope("cases:read"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        requirements = requirements_engine.discover(
            case.objective,
            case.customer_type,
            case.jurisdiction,
            case.inputs,
        )
        required = requirements_engine.document_request(requirements)["documents"]
        submitted = {
            str(document.get("type")) if isinstance(document, dict) else str(document)
            for document in case.inputs.get("documents", [])
        }
        return {
            "case_id": case_id,
            "required_documents": required,
            "submitted_documents": sorted(submitted),
            "missing_documents": [doc for doc in required if doc not in submitted],
            "ready_to_execute": all(doc in submitted for doc in required),
        }
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.get("/rules/readiness")
def rules_readiness():
    services = engine.services.all()
    source_backed = len(rule_registry.all())
    return {
        "status": "development",
        "services_in_catalog": len(services),
        "source_backed_rule_records": source_backed,
        "production_legal_coverage_complete": False,
        "note": "Aether blocks no service because baseline metadata is explicitly non-authoritative; production execution must use verified, effective-dated rules for the target jurisdiction."
    }


@router.post("/api-keys")
def create_api_key(data: Dict[str, Any] | None = None, principal: Principal = Depends(require_scope("cases:write"))):
    """Create one tenant-scoped developer key; the raw secret is returned once."""
    if principal.auth_mode == "none":
        tenant_id = principal.tenant_id or "demo"
    else:
        tenant_id = principal.tenant_id
        if principal.role.lower() not in {"admin", "developer", "business", "bank", "enterprise", "insurer"}:
            raise HTTPException(status_code=403, detail="This role cannot create API keys")
    if not tenant_id:
        raise HTTPException(status_code=403, detail="Active tenant is required")

    data = data or {}
    requested_role = str(data.get("role", "service")).lower()
    # API keys are machine credentials, never delegated government officer/admin roles.
    # Human/administrative authority remains bound to Supabase Auth + membership.
    if requested_role not in {"service", "integration", "developer"}:
        raise HTTPException(status_code=400, detail="API key role must be service, integration, or developer")
    role = requested_role
    scopes = data.get("scopes") or ["cases:read", "cases:write"]
    if not isinstance(scopes, list) or not all(isinstance(scope, str) for scope in scopes):
        raise HTTPException(status_code=400, detail="scopes must be a list of strings")
    allowed_scopes = {"cases:read", "cases:write", "documents:read", "documents:write", "payments:read", "payments:write", "analytics:read"}
    if any(scope not in allowed_scopes for scope in scopes):
        raise HTTPException(status_code=400, detail="Unsupported API scope")

    raw_key = "aether_" + secrets.token_urlsafe(32)
    key_prefix = raw_key[:20]
    key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    try:
        from datetime import datetime, timedelta
        with SessionLocal() as db:
            from .persistence_models import AetherApiKeyRecord
            row = AetherApiKeyRecord(
                tenant_id=tenant_id,
                key_prefix=key_prefix,
                key_hash=key_hash,
                role=role,
                scopes=scopes,
                status="active",
                created_at=datetime.utcnow(),
                expires_at=(
                    datetime.utcnow() + timedelta(days=int(data["expires_in_days"]))
                    if data.get("expires_in_days") else None
                ),
            )
            db.add(row)
            db.commit()
        return {
            "key": raw_key,
            "key_prefix": key_prefix,
            "tenant_id": tenant_id,
            "role": role,
            "scopes": scopes,
            "warning": "Store the raw API key now; Aether never returns it again.",
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail="API key store unavailable") from exc


@router.post("/api-keys/{key_prefix}/revoke")
def revoke_api_key(key_prefix: str, principal: Principal = Depends(require_scope("cases:write"))):
    if not principal.tenant_id:
        raise HTTPException(status_code=403, detail="Active tenant is required")
    try:
        from .persistence_models import AetherApiKeyRecord
        with SessionLocal() as db:
            row = db.query(AetherApiKeyRecord).filter_by(
                tenant_id=principal.tenant_id,
                key_prefix=key_prefix,
            ).one_or_none()
            if not row:
                raise HTTPException(status_code=404, detail="API key not found")
            row.status = "revoked"
            db.commit()
            return {"status": "revoked", "key_prefix": row.key_prefix}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="API key store unavailable") from exc


@router.get("/api-keys")
def list_api_keys(principal: Principal = Depends(require_scope("cases:read"))):
    if not principal.tenant_id:
        raise HTTPException(status_code=403, detail="Active tenant is required")
    try:
        from .persistence_models import AetherApiKeyRecord
        with SessionLocal() as db:
            rows = db.query(AetherApiKeyRecord).filter(
                AetherApiKeyRecord.tenant_id == principal.tenant_id
            ).order_by(AetherApiKeyRecord.created_at.desc()).all()
            return {"keys": [{
                "key_prefix": row.key_prefix,
                "tenant_id": row.tenant_id,
                "role": row.role,
                "scopes": row.scopes or [],
                "status": row.status,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "expires_at": row.expires_at.isoformat() if row.expires_at else None,
                "last_used_at": row.last_used_at.isoformat() if row.last_used_at else None,
            } for row in rows]}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="API key store unavailable") from exc


@router.get("/admin/memberships")
def list_memberships(principal: Principal = Depends(require_role("admin"))):
    if engine.store is None:
        raise HTTPException(status_code=503, detail="Membership store unavailable")
    try:
        with SessionLocal() as db:
            rows = db.execute(text(
                "SELECT user_id, tenant_id, role, status, department, jurisdiction, created_at, updated_at "
                "FROM public.aether_memberships ORDER BY created_at DESC LIMIT 500"
            )).mappings().all()
            return {"memberships": [dict(row) for row in rows]}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Membership store unavailable") from exc


@router.post("/admin/memberships")
def set_membership(data: Dict[str, Any], principal: Principal = Depends(require_role("admin"))):
    required = {"user_id", "tenant_id", "role"}
    if not required.issubset(data):
        raise HTTPException(status_code=400, detail="user_id, tenant_id and role are required")
    allowed_roles = {"user", "citizen", "business", "bank", "developer", "insurer", "enterprise", "officer", "department_admin", "admin"}
    role = str(data["role"]).lower()
    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail="Unsupported Aether role")
    try:
        with SessionLocal() as db:
            db.execute(text(
                "INSERT INTO public.aether_memberships "
                "(user_id, tenant_id, role, status, department, jurisdiction, updated_at) "
                "VALUES (:user_id, :tenant_id, :role, :status, :department, CAST(:jurisdiction AS jsonb), now()) "
                "ON CONFLICT (user_id, tenant_id) DO UPDATE SET "
                "role = EXCLUDED.role, status = EXCLUDED.status, department = EXCLUDED.department, "
                "jurisdiction = EXCLUDED.jurisdiction, updated_at = now()"
            ), {
                "user_id": data["user_id"],
                "tenant_id": data["tenant_id"],
                "role": role,
                "status": str(data.get("status", "active")),
                "department": data.get("department"),
                "jurisdiction": __import__("json").dumps(data.get("jurisdiction") or {}),
            })
            db.commit()
        return {"status": "updated", "user_id": data["user_id"], "tenant_id": data["tenant_id"], "role": role}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Membership store unavailable") from exc


@router.get("/cases/{case_id}/documents")
def case_documents(case_id: str, principal: Principal = Depends(require_scope("documents:read"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return {"documents": engine.store.documents_for(case_id, case.tenant_id)}
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/documents/upload")
def upload_case_document(
    case_id: str,
    document_type: str,
    file: UploadFile = File(...),
    principal: Principal = Depends(require_scope("documents:write")),
):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        requirements = requirements_engine.discover(
            case.objective,
            case.customer_type,
            case.jurisdiction,
            case.inputs,
        )
        required_documents = requirements_engine.document_request(requirements)["documents"]
        if document_type not in required_documents:
            raise HTTPException(
                status_code=400,
                detail=f"Document type is not required for this case: {document_type}",
            )

        content = file.file.read()
        stored = document_store.save(
            case_id=case_id,
            tenant_id=case.tenant_id or principal.tenant_id,
            document_type=document_type,
            filename=file.filename or "document",
            content=content,
            mime_type=file.content_type,
        )
        engine.store.put_document(stored, owner_user_id=principal.subject)
        case.inputs.setdefault("documents", []).append({
            "type": document_type,
            "document_id": stored.document_id,
            "filename": stored.filename,
            "mime_type": stored.mime_type,
            "size_bytes": stored.size_bytes,
            "sha256": stored.sha256,
            "storage_key": stored.storage_key,
            "text": stored.extracted_text,
            "extraction_mode": stored.extraction_mode,
        })
        engine.store.put(case)

        submitted_types = {
            str(document.get("type")) if isinstance(document, dict) else str(document)
            for document in case.inputs.get("documents", [])
        }
        missing = [doc for doc in required_documents if doc not in submitted_types]

        notification_service.enqueue(
            case.tenant_id or principal.tenant_id,
            principal.subject,
            case_id,
            "document.uploaded",
            "in_app",
            payload={"document_id": stored.document_id, "document_type": document_type},
        )
        if missing:
            return {
                "status": "uploaded",
                "case_status": "needs_documents",
                "missing_documents": missing,
                "document": document_summary(stored),
                "case": serialize(case, include_tasks=False),
            }

        resumed = engine.execute_until_pause(case_id)
        return {
            "status": "uploaded_and_resumed",
            "case_status": resumed.status,
            "missing_documents": [],
            "document": document_summary(stored),
            "case": serialize(resumed, include_tasks=False),
        }
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except OSError as exc:
        raise HTTPException(status_code=400, detail=f"Unable to store document: {exc}")


@router.get("/cases/{case_id}/documents/{document_id}/download")
def download_case_document(case_id: str, document_id: str, principal: Principal = Depends(require_scope("documents:read"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        docs = engine.store.documents_for(case_id, case.tenant_id)
        metadata = next((item for item in docs if item["document_id"] == document_id), None)
        if not metadata:
            raise HTTPException(status_code=404, detail="Document not found")

        from .persistence_models import AetherDocumentRecord
        with SessionLocal() as db:
            row = db.query(AetherDocumentRecord).filter_by(
                document_id=document_id,
                case_id=case_id,
                tenant_id=case.tenant_id,
            ).one_or_none()
            if not row:
                raise HTTPException(status_code=404, detail="Document not found")
            storage_key = row.storage_key
            mime_type = row.mime_type
            filename = row.filename

        payload = document_store.read(storage_key)
        import hashlib
        digest = hashlib.sha256(payload).hexdigest()
        if digest != metadata["sha256"]:
            raise HTTPException(status_code=409, detail="Document integrity check failed")
        return Response(
            content=payload,
            media_type=mime_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Document-SHA256": digest,
            },
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.get("/usage")
def usage_summary(
    principal: Principal = Depends(require_principal),
):
    tenant_id = principal.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=403, detail="Active tenant is required for usage reporting")
    return engine.store.usage_summary(tenant_id)


@router.get("/rules")
def rule_catalog():
    return {
        "count": len(rule_registry.all()),
        "rules": rule_registry.all(),
    }


@router.get("/services")
def service_catalog():
    return {
        "count": len(engine.services.all()),
        "services": engine.services.catalog(),
    }


@router.post("/understand")
def understand(request: StartCaseRequest):
    return understanding_engine.understand(
        request.objective,
        request.customer_type,
        request.jurisdiction,
    ).as_dict()


@router.post("/requirements")
def discover_requirements(request: StartCaseRequest):
    requirements = requirements_engine.discover(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        request.inputs,
    )
    required_documents = requirements_engine.document_request(requirements)
    submitted = set(request.inputs.get("documents", []))
    missing = [doc for doc in required_documents["documents"] if doc not in submitted]
    return {
        "requirements": [r.__dict__ for r in requirements],
        "documents": required_documents["documents"],
        "submitted_documents": sorted(submitted),
        "missing_documents": missing,
        "ready_to_execute": not missing,
    }


@router.get("/me")
def current_principal(principal: Principal = Depends(require_principal)):
    """Return the server-resolved Aether identity and authorization scope."""
    return {
        "subject": principal.subject,
        "role": principal.role,
        "tenant_id": principal.tenant_id,
        "department": principal.department,
        "jurisdiction": principal.jurisdiction,
        "auth_mode": principal.auth_mode,
    }


@router.post("/cases")
def start_case(request: StartCaseRequest, principal: Principal = Depends(require_scope("cases:write"))):
    understanding = understanding_engine.understand(
        request.objective,
        request.customer_type,
        request.jurisdiction,
    )

    if understanding.service_id is None or understanding.ambiguous:
        return {
            "status": "needs_clarification",
            "objective": request.objective,
            "understanding": understanding.as_dict(),
            "candidates": understanding.candidates,
            "requirements": [],
        }

    requirements = requirements_engine.discover(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        request.inputs,
    )
    required_documents = requirements_engine.document_request(requirements)
    submitted = set(request.inputs.get("documents", []))
    missing = [doc for doc in required_documents["documents"] if doc not in submitted]

    if missing:
        case = engine.create_case(
            request.objective,
            request.customer_type,
            request.jurisdiction,
            {**request.inputs, "enforce_intake_gate": True},
            owner_user_id=principal.subject,
            tenant_id=principal.tenant_id or principal.subject,
        )
        case.requirements = [r.__dict__ for r in requirements]
        case.status = "needs_documents"
        engine.store.put(case)
        response = serialize(case, include_tasks=False)
        response.update({
            "status": "needs_documents",
            "documents": required_documents["documents"],
            "missing_documents": missing,
        })
        return response

    case = engine.create_case(
        request.objective,
        request.customer_type,
        request.jurisdiction,
        {**request.inputs, "enforce_intake_gate": True},
        owner_user_id=principal.subject,
        tenant_id=principal.tenant_id or principal.subject,
    )
    case.requirements = [r.__dict__ for r in requirements]
    case = engine.execute_until_pause(case.case_id)
    notification_service.enqueue(
        case.tenant_id or principal.tenant_id,
        principal.subject,
        case.case_id,
        "case.started",
        "in_app",
        payload={"status": case.status, "service_id": case.service_id},
    )
    return serialize(case)


def _authorize_case(case, principal: Principal) -> None:
    if principal.auth_mode == "none" or principal.role.lower() == "admin":
        return
    same_owner = case.owner_user_id and case.owner_user_id == principal.subject
    same_tenant = case.tenant_id and principal.tenant_id and case.tenant_id == principal.tenant_id
    if principal.auth_mode == "api_key" and same_tenant:
        return
    if principal.role.lower() in {"officer", "department_admin"} and same_tenant:
        if principal.department and case.service_department:
            if principal.department.lower() != case.service_department.lower():
                raise HTTPException(status_code=404, detail="Case not found")
        for key, value in (principal.jurisdiction or {}).items():
            if value and case.jurisdiction.get(key) and case.jurisdiction.get(key) != value:
                raise HTTPException(status_code=404, detail="Case not found")
        return
    if same_owner and (not case.tenant_id or not principal.tenant_id or same_tenant):
        return
    raise HTTPException(status_code=404, detail="Case not found")


def _list_visible_cases(
    principal: Principal,
    status: str | None = None,
    limit: int = 50,
):
    safe_limit = max(1, min(limit, 100))
    if principal.role.lower() == "admin" or principal.auth_mode == "none":
        return engine.store.list(status=status, limit=safe_limit)

    if principal.role.lower() in {"officer", "department_admin"} and principal.tenant_id:
        candidates = engine.store.list(
            tenant_id=principal.tenant_id,
            status=status,
            limit=100,
        )
        visible = []
        for summary in candidates:
            try:
                _authorize_case(engine.get_case(summary["case_id"]), principal)
            except HTTPException:
                continue
            visible.append(summary)
        return visible[:safe_limit]

    return engine.store.list(
        owner_user_id=principal.subject,
        status=status,
        limit=safe_limit,
    )


@router.get("/cases")
def list_cases(
    status: str | None = None,
    limit: int = 50,
    principal: Principal = Depends(require_scope("cases:read")),
):
    return {"cases": _list_visible_cases(principal, status=status, limit=limit)}


@router.post("/cases/{case_id}/documents")
def submit_case_documents(
    case_id: str,
    request: DocumentSubmissionRequest,
    principal: Principal = Depends(require_scope("documents:write")),
):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)

        existing = list(case.inputs.get("documents", []))
        combined = existing + list(request.documents)
        deduped = []
        seen = set()
        for document in combined:
            key = str(document.get("type")) if isinstance(document, dict) else str(document)
            fingerprint = (key, repr(document))
            if fingerprint not in seen:
                seen.add(fingerprint)
                deduped.append(document)

        case.inputs["documents"] = deduped
        case.inputs["enforce_intake_gate"] = True
        requirements = requirements_engine.discover(
            case.objective,
            case.customer_type,
            case.jurisdiction,
            case.inputs,
        )
        case.requirements = [r.__dict__ for r in requirements]
        required_documents = requirements_engine.document_request(requirements)
        submitted_types = {
            str(document.get("type")) if isinstance(document, dict) else str(document)
            for document in deduped
        }
        missing = [doc for doc in required_documents["documents"] if doc not in submitted_types]
        if missing:
            case.status = "needs_documents"
            engine.store.put(case)
            response = serialize(case, include_tasks=False)
            response.update({
                "status": "needs_documents",
                "documents": required_documents["documents"],
                "missing_documents": missing,
            })
            return response

        return serialize(engine.execute_until_pause(case_id))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/resume")
def resume_case(case_id: str, principal: Principal = Depends(require_scope("cases:write"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return serialize(engine.execute_until_pause(case_id))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.get("/cases/{case_id}/audit")
def case_audit_integrity(case_id: str, principal: Principal = Depends(require_scope("cases:read"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        from .audit import AuditTrail
        events = engine.store.events_for(case_id)
        return {
            "case_id": case_id,
            "integrity": AuditTrail.verify_chain(events),
        }
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.get("/cases/{case_id}/events")
def case_events(case_id: str, principal: Principal = Depends(require_scope("cases:read"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return {"case_id": case_id, "events": engine.store.events_for(case_id)}
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.get("/cases/{case_id}")
def get_case(case_id: str, principal: Principal = Depends(require_scope("cases:read"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        return serialize(case)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/human/{task_id}")
def human_decision(case_id: str, task_id: str, request: HumanDecisionRequest, principal: Principal = Depends(require_role("officer", "department_admin", "admin"))):
    try:
        case = engine.get_case(case_id)
        _authorize_case(case, principal)
        decision = "approved" if request.approved else "rejected"
        case = engine.complete_human_task(
            case_id,
            task_id,
            decision,
            request.note or "",
            actor_id=principal.subject,
            actor_role=principal.role,
        )
        return serialize(case)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case or task not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
