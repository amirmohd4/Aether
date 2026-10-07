"""Test bootstrap for the backend package layout.

The application is executed as backend.main in containers while older tests
import aether_core from the backend working directory. Alias both names to one
module tree so SQLAlchemy sees one declarative metadata registry.
"""

from __future__ import annotations

import sys

import backend.aether_core as canonical

sys.modules.setdefault("aether_core", canonical)

for name, module in list(sys.modules.items()):
    if name.startswith("backend.aether_core."):
        sys.modules.setdefault(name.replace("backend.", "", 1), module)
