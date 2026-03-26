# API Routes package
from .property_routes import router as property_router
from .workflow_routes import router as workflow_router
from .fraud_routes import router as fraud_router
from .certificate_routes import router as certificate_router
from .system_routes import router as system_router

__all__ = [
    "property_router",
    "workflow_router",
    "fraud_router",
    "certificate_router",
    "system_router"
]
