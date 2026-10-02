from fastapi import FastAPI
from .api.property_routes import router as property_router
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Aether GovOS API",
    description="Outcome-driven government execution platform",
    version="0.2.0-aether-v2",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.api.billing_routes import router as billing_router
from backend.api.workflow_routes import router as workflow_router
from backend.api.fraud_routes import router as fraud_router
from backend.api.water_connection_routes import router as water_router
from backend.api.aether_routes import router as aether_router

app.include_router(billing_router, prefix="/api/billing", tags=["Billing"])
app.include_router(property_router)
app.include_router(workflow_router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(fraud_router, prefix="/api/fraud", tags=["Fraud"])
app.include_router(water_router, prefix="/api/water-connection", tags=["Water Connection"])
app.include_router(aether_router, prefix="/api/aether", tags=["Aether Execution"])


@app.get("/")
async def root():
    return {
        "service": "Aether GovOS",
        "status": "running",
        "version": "0.2.0-aether-v2",
        "core": "objective -> case -> work graph -> execution -> human authority -> outcome",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "aether_core": "ready"}
