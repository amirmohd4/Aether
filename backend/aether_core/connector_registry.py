from __future__ import annotations

from typing import Dict, List

from .connectors import GovernmentConnector, SyntheticConnector
from .synthetic_government import SyntheticGovernmentSystem


class ConnectorRegistry:
    """Department connector resolver.

    The MVP defaults to deterministic synthetic connectors. Production adapters
    are registered explicitly so authorization and integration boundaries are
    visible instead of hidden inside worker code.
    """

    def __init__(self, synthetic_system: SyntheticGovernmentSystem | None = None):
        self._synthetic_system = synthetic_system or SyntheticGovernmentSystem()
        self._connectors: Dict[str, GovernmentConnector] = {}

    def register(self, department: str, connector: GovernmentConnector) -> None:
        self._connectors[department] = connector

    def get(self, department: str) -> GovernmentConnector:
        if department not in self._connectors:
            self._connectors[department] = SyntheticConnector(
                department,
                system=self._synthetic_system,
            )
        return self._connectors[department]

    def catalog(self) -> List[dict]:
        return [
            {
                "department": department,
                "connector": connector.__class__.__name__,
                "mode": "synthetic" if isinstance(connector, SyntheticConnector) else "production",
            }
            for department, connector in sorted(self._connectors.items())
        ]
