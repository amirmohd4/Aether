import time
import hashlib
from typing import Dict, Any, List

class AuditLogService:
    """Immutable audit trail logger for sovereign government transactions."""
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def record_transaction(self, country_code: str, service_id: str, actor: str, status: str, details: Dict[str, Any]) -> Dict[str, Any]:
        prev_hash = self.logs[-1]["log_hash"] if self.logs else "0" * 64
        timestamp = int(time.time())
        
        raw_string = f"{prev_hash}:{timestamp}:{country_code}:{service_id}:{actor}:{status}"
        log_hash = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
        
        entry = {
            "log_id": f"AUDIT-{len(self.logs) + 1:06d}",
            "timestamp": timestamp,
            "country_code": country_code,
            "service_id": service_id,
            "actor": actor,
            "status": status,
            "details": details,
            "previous_hash": prev_hash,
            "log_hash": log_hash
        }
        self.logs.append(entry)
        return entry

    def get_audit_trail(self, country_code: str = None) -> List[Dict[str, Any]]:
        if country_code:
            return [log for log in self.logs if log["country_code"].lower() == country_code.lower()]
        return self.logs

audit_service = AuditLogService()
