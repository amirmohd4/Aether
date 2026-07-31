from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddlewar
from api.config_routes import router as config_router
from api.language_routes import router as language_router
from api.api_key_routes import router as api_key_router
from api.billing_routes import router as billing_router
from api.workflow_routes import router as workflow_router
app = FastAPI(
    title="Aether - Global Digital Governance Engine",
    description="Configurable sovereign government service API, GovStack 2.0 building blocks, and developer portal",
    version="2.0.0"
)

# Enable CORS for all origins for global frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(config_router)
app.include_router(language_router)
app.include_router(api_key_router)
app.include_router(billing_router)
app.include_router(workflow_router)

@app.get("/")
def root():
    return {
        "engine": "Aether Sovereign Global Layer",
        "version": "2.0.0",
        "status": "HEALTHY",
        "govstack_compliance": "GovStack 2.0 Certified"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
