from __future__ import annotations

import time
from typing import Any, Dict

from .engine import AetherExecutionEngine


class AetherWorkerRuntime:
    """Operational worker loop for resumable cases.

    The web API remains the synchronous demo surface; this runtime provides a
    deployable worker process that can resume queued/waiting cases from the
    durable repository.
    """

    def __init__(self, engine: AetherExecutionEngine | None = None) -> None:
        self.engine = engine or AetherExecutionEngine()

    def run_once(self, limit: int = 25) -> Dict[str, Any]:
        candidates = self.engine.store.list(limit=max(1, min(limit, 100)))
        processed = []
        for summary in candidates:
            if summary.get("status") in {"executing", "waiting", "exception"}:
                try:
                    case = self.engine.execute_until_pause(summary["case_id"])
                    processed.append({
                        "case_id": case.case_id,
                        "status": case.status,
                    })
                except Exception as exc:
                    processed.append({
                        "case_id": summary["case_id"],
                        "status": "error",
                        "error": str(exc),
                    })
        return {"processed": processed, "count": len(processed)}

    def run_forever(self, interval_seconds: int = 5) -> None:
        while True:
            self.run_once()
            time.sleep(max(1, interval_seconds))
