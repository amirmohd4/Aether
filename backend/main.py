from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app FIRST
app = FastAPI(
    title="Aether GovOS API",
    description="Sovereign Government Operating System Backend",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers AFTER app is created (breaks circular imports)
from backend.api.billing_routes import router as billing_router
from backend.api.workflow_routes import router as workflow_router
from backend.api.fraud_routes import router as fraud_router
from backend.api.connector_routes import router as connector_router

# Register routers
app.include_router(billing_router, prefix="/api/billing", tags=["Billing"])
app.include_router(workflow_router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(fraud_router, prefix="/api/fraud", tags=["Fraud"])
app.include_router(connector_router, prefix="/api/connectors", tags=["Connectors"])

@app.get("/")
async def root():
    return {
        "service": "Aether GovOS",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
