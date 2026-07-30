import time
from typing import Dict, Tuple

class RateLimiter:
    """Sliding window rate limiter middleware for Aether API requests."""
    def __init__(self):
        # Stores key_id -> list of timestamps
        self.request_history: Dict[str, list] = {}

    def is_allowed(self, key_id: str, max_requests: int = 100, window_seconds: int = 60) -> Tuple[bool, int]:
        now = time.time()
        cutoff = now - window_seconds
        
        if key_id not in self.request_history:
            self.request_history[key_id] = []
            
        # Clean up old timestamps
        self.request_history[key_id] = [t for t in self.request_history[key_id] if t > cutoff]
        
        current_count = len(self.request_history[key_id])
        if current_count >= max_requests:
            remaining = max_requests - current_count
            return False, remaining
            
        self.request_history[key_id].append(now)
        return True, max_requests - current_count - 1

rate_limiter = RateLimiter()
