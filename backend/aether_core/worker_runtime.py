from __future__ import annotations

import os
import socket
import time
from typing import Any, Dict

from .engine import AetherExecutionEngine
from .notifications import NotificationService
from backend.database import SessionLocal


class AetherWorkerRuntime:
    """Operational worker with durable case leases and notification dispatch."""

    def __init__(self, engine: AetherExecutionEngine | None = None) -> None:
        self.engine = engine or AetherExecutionEngine()
        self.notifications = NotificationService(SessionLocal)
        self.worker_id = os.getenv(
            "AETHER_WORKER_ID",
            f"{socket.gethostname()}:{os.getpid()}",
        )

    def run_once(self, limit: int = 25) -> Dict[str, Any]:
        candidates = self.engine.store.list(limit=max(1, min(limit, 100)))
        processed = []
        for summary in candidates:
            if summary.get("status") not in {"executing", "waiting", "exception"}:
                continue

            case_id = summary["case_id"]
            if not self.engine.store.try_claim_case(
                case_id,
                self.worker_id,
                lease_seconds=300,
            ):
                continue

            try:
                case = self.engine.execute_until_pause(
                    case_id,
                    lease_owner=self.worker_id,
                    lease_seconds=300,
                )
                processed.append({
                    "case_id": case.case_id,
                    "status": case.status,
                })
            except Exception as exc:
                processed.append({
                    "case_id": case_id,
                    "status": "error",
                    "error": str(exc),
                })
            finally:
                self.engine.store.release_case(case_id, self.worker_id)

        dispatch = self.notifications.dispatch_queued()
        return {
            "processed": processed,
            "count": len(processed),
            "notifications": dispatch,
        }

    def run_forever(self, interval_seconds: int = 5) -> None:
        while True:
            self.run_once()
            time.sleep(max(1, interval_seconds))
