from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.config_routes import router as config_router
from backend.api.language_routes import router as language_router
from backend.api.api_key_routes import router as api_key_router
from backend.api.billing_routes import router as billing_router
from backend.api.workflow_routes import router as workflow_router
from backend.database import init_db

app = FastAPI(
    title="Aether - Global Digital Governance Engine",
    description="Configurable sovereign government service API, GovStack 2.0 building blocks, and developer portal",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router)
app.include_router(language_router)
app.include_router(api_key_router)
app.include_router(billing_router)
app.include_router(workflow_router)

@app.get("/")
def root():
    return {
        "name": "Aether GovOS",
        "version": "1.0.0",
        "description": "Government Integration Operating System",
        "tagline": "One API for all government services",
        "documentation": "/api/docs",
        "health": "/api/system/health"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "Aether GovOS"}

@app.on_event("startup")
def startup():
    print("🚀 Starting Aether GovOS...")
    init_db()
    print("✅ Aether GovOS started successfully")
