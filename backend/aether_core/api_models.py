from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class StartCaseRequest(BaseModel):
    objective: str = Field(min_length=5)
    customer_type: str = "business"
    jurisdiction: Dict[str, str] = Field(default_factory=dict)
    inputs: Dict[str, Any] = Field(default_factory=dict)


class HumanDecisionRequest(BaseModel):
    approved: bool
    note: Optional[str] = None
