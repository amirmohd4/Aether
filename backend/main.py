from fastapi import FastAPI
from .api.property_routes import router as property_router
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

# Import ONLY the routers that ACTUALLY exist in your folder
from backend.api.billing_routes import router as billing_router
from backend.api.workflow_routes import router as workflow_router
from backend.api.fraud_routes import router as fraud_router
from backend.api.water_connection_routes import router as water_router  # <-- THIS EXISTS
# from backend.api.connector_routes import router as connector_router  # <-- COMMENT THIS - DOESN'T EXIST

# Register routers that exist
app.include_router(billing_router, prefix="/api/billing", tags=["Billing"])
app.include_router(property_router)
app.include_router(workflow_router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(fraud_router, prefix="/api/fraud", tags=["Fraud"])
app.include_router(water_router, prefix="/api/water-connection", tags=["Water Connection"])
# app.include_router(connector_router, prefix="/api/connectors", tags=["Connectors"])  # <-- COMMENT THIS

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
