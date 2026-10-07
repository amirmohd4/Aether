from __future__ import annotations

import base64
import hashlib
import mimetypes
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

import httpx

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional dependency fallback
    PdfReader = None


@dataclass(frozen=True)
class StoredDocument:
    document_id: str
    case_id: str
    tenant_id: str | None
    document_type: str
    filename: str
    mime_type: str
    size_bytes: int
    sha256: str
    storage_key: str
    extracted_text: str
    extraction_mode: str
    created_at: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DocumentStore:
    """Server-side document store with a local fallback and Supabase Storage adapter."""

    def __init__(self) -> None:
        self.bucket = os.getenv("AETHER_DOCUMENT_BUCKET", "aether-documents")
        self.root = Path(os.getenv("AETHER_DOCUMENT_ROOT", "./data/documents"))
        self.supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    def save(
        self,
        case_id: str,
        tenant_id: str | None,
        document_type: str,
        filename: str,
        content: bytes,
        mime_type: str | None = None,
    ) -> StoredDocument:
        if not content:
            raise ValueError("Document is empty")
        if len(content) > self._max_bytes():
            raise ValueError("Document exceeds the configured upload limit")

        document_id = f"DOC-{uuid4().hex[:16].upper()}"
        safe_name = Path(filename or "document").name
        resolved_mime = mime_type or mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
        allowed = {
            item.strip() for item in os.getenv(
                "AETHER_ALLOWED_DOCUMENT_MIME_TYPES",
                "application/pdf,text/plain,text/csv,application/json,image/jpeg,image/png,"
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ).split(",") if item.strip()
        }
        if resolved_mime not in allowed:
            raise ValueError(f"Unsupported document type: {resolved_mime}")
        digest = hashlib.sha256(content).hexdigest()
        storage_key = f"{tenant_id or 'unscoped'}/{case_id}/{document_id}-{safe_name}"

        if self._supabase_configured():
            self._save_supabase(storage_key, content, resolved_mime)
            storage_ref = f"supabase://{self.bucket}/{storage_key}"
        else:
            target = self.root / storage_key
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            storage_ref = str(target)

        extracted_text, extraction_mode = self._extract(
            safe_name,
            resolved_mime,
            content,
        )
        return StoredDocument(
            document_id=document_id,
            case_id=case_id,
            tenant_id=tenant_id,
            document_type=document_type,
            filename=safe_name,
            mime_type=resolved_mime,
            size_bytes=len(content),
            sha256=digest,
            storage_key=storage_ref,
            extracted_text=extracted_text,
            extraction_mode=extraction_mode,
            created_at=__import__("datetime").datetime.utcnow().isoformat() + "Z",
        )

    def read(self, storage_key: str) -> bytes:
        if storage_key.startswith("supabase://"):
            _, remainder = storage_key.split("supabase://", 1)
            bucket, key = remainder.split("/", 1)
            if not self._supabase_configured():
                raise RuntimeError("Supabase document storage is not configured")
            response = httpx.get(
                f"{self.supabase_url}/storage/v1/object/{bucket}/{key}",
                headers=self._headers(),
                timeout=20.0,
            )
            response.raise_for_status()
            return response.content
        return Path(storage_key).read_bytes()

    def _supabase_configured(self) -> bool:
        return bool(self.supabase_url and self.service_key)

    def _headers(self, content_type: str | None = None) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.service_key}",
            "apikey": self.service_key,
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _save_supabase(self, key: str, content: bytes, mime_type: str) -> None:
        response = httpx.post(
            f"{self.supabase_url}/storage/v1/object/{self.bucket}/{key}",
            content=content,
            headers=self._headers(mime_type),
            timeout=30.0,
        )
        response.raise_for_status()

    @staticmethod
    def _max_bytes() -> int:
        return max(1, int(os.getenv("AETHER_MAX_DOCUMENT_BYTES", str(15 * 1024 * 1024))))

    def _extract(self, filename: str, mime_type: str, content: bytes) -> tuple[str, str]:
        if mime_type.startswith("text/") or mime_type in {"application/json", "application/xml"}:
            return content.decode("utf-8", errors="replace"), "native-text"

        if mime_type == "application/pdf" and PdfReader is not None:
            try:
                reader = PdfReader(__import__("io").BytesIO(content))
                text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
                if text:
                    return text, "pdf-text"
            except Exception:
                pass

        ocr_base = os.getenv("AETHER_OCR_BASE_URL", "").strip().rstrip("/")
        ocr_token = os.getenv("AETHER_OCR_TOKEN", "").strip()
        if ocr_base:
            payload = {
                "filename": filename,
                "mime_type": mime_type,
                "content_base64": base64.b64encode(content).decode("ascii"),
            }
            headers = {"Content-Type": "application/json"}
            if ocr_token:
                headers["Authorization"] = f"Bearer {ocr_token}"
            response = httpx.post(
                f"{ocr_base}/extract",
                json=payload,
                headers=headers,
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return str(data.get("text", "")), str(data.get("mode", "external-ocr"))

        return "", "metadata-only"


def document_summary(document: StoredDocument) -> Dict[str, Any]:
    payload = document.as_dict()
    payload.pop("extracted_text", None)
    return payload
