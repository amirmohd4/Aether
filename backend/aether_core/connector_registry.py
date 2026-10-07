from __future__ import annotations

import json
import os
from typing import Dict, List

from .connectors import ConfiguredHTTPConnector, GovernmentConnector, SyntheticConnector
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
        self._load_configured_production_connectors()

    def _load_configured_production_connectors(self) -> None:
        """Load explicitly opted-in production connector configs from env."""
        if os.getenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "").strip().lower() != "true":
            return
        raw = os.getenv("AETHER_PRODUCTION_CONNECTORS", "").strip()
        if not raw:
            return
        try:
            configs = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("AETHER_PRODUCTION_CONNECTORS must be valid JSON") from exc
        if not isinstance(configs, dict):
            raise RuntimeError("AETHER_PRODUCTION_CONNECTORS must be an object")
        for department, config in configs.items():
            if not isinstance(config, dict) or not config.get("base_url"):
                raise RuntimeError(f"Production connector config for {department} needs base_url")
            if not config.get("bearer_token"):
                raise RuntimeError(
                    f"Production connector config for {department} needs bearer_token"
                )
            base_url = str(config["base_url"]).rstrip("/")
            if not base_url.startswith("https://"):
                raise RuntimeError(
                    f"Production connector config for {department} must use HTTPS"
                )
            self.register(
                department,
                ConfiguredHTTPConnector(
                    department=department,
                    base_url=base_url,
                    bearer_token=str(config["bearer_token"]) if config.get("bearer_token") else None,
                    timeout_seconds=float(config.get("timeout_seconds", 10)),
                ),
            )

    def register(self, department: str, connector: GovernmentConnector) -> None:
        self._connectors[department] = connector

    def get(self, department: str) -> GovernmentConnector:
        if department not in self._connectors:
            self._connectors[department] = SyntheticConnector(
                department,
                system=self._synthetic_system,
            )
        return self._connectors[department]

    def production_configured(self) -> bool:
        return any(
            isinstance(connector, ConfiguredHTTPConnector)
            and connector.configuration_valid()
            for connector in self._connectors.values()
        )

    def is_production(self, department: str) -> bool:
        """Return whether a department has an explicitly configured live connector."""
        return not isinstance(self.get(department), SyntheticConnector)

    def catalog(self) -> List[dict]:
        return [
            {
                "department": department,
                "connector": connector.__class__.__name__,
                "mode": "synthetic" if isinstance(connector, SyntheticConnector) else "production",
            }
            for department, connector in sorted(self._connectors.items())
        ]
