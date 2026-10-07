from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
import time
from collections import defaultdict, deque
from uuid import uuid4

from backend.api.property_routes import router as property_router
from backend.api.billing_routes import router as billing_router
from backend.api.workflow_routes import router as workflow_router
from backend.api.fraud_routes import router as fraud_router
from backend.api.water_connection_routes import router as water_router
from backend.api.aether_routes import router as aether_router
from backend.aether_core.routes import router as aether_v2_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Aether GovOS API",
    description="Outcome-driven government execution platform",
    version="0.4.0-aether-mvp",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "AETHER_CORS_ORIGINS",
        "http://localhost:5173,https://aether-govos.netlify.app",
    ).split(",")
    if origin.strip()
]

_rate_windows = defaultdict(deque)


@app.middleware("http")
async def platform_hardening(request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    production = os.getenv("AETHER_ENV", "development").strip().lower() == "production"

    limit = max(30, int(os.getenv("AETHER_RATE_LIMIT_PER_MINUTE", "300")))
    client_host = request.client.host if request.client else "unknown"
    now = time.monotonic()
    bucket = _rate_windows[client_host]
    while bucket and now - bucket[0] >= 60:
        bucket.popleft()
    if production and len(bucket) >= limit:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded", "request_id": request_id},
            headers={"Retry-After": "60", "X-Request-ID": request_id},
        )
    bucket.append(now)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if production:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

legacy_api_enabled = os.getenv(
    "AETHER_ENABLE_LEGACY_API",
    "false" if os.getenv("AETHER_ENV", "development").strip().lower() == "production" else "true",
).strip().lower() == "true"

if legacy_api_enabled:
    app.include_router(billing_router, prefix="/api/billing", tags=["Billing"])
    app.include_router(property_router)
    app.include_router(workflow_router, prefix="/api/workflow", tags=["Workflow"])
    app.include_router(fraud_router, prefix="/api/fraud", tags=["Fraud"])
    app.include_router(water_router, prefix="/api/water-connection", tags=["Water Connection"])
    app.include_router(aether_router, prefix="/api/aether", tags=["Aether Execution"])

app.include_router(aether_v2_router)


@app.get("/")
async def root():
    return {
        "service": "Aether GovOS",
        "status": "running",
        "version": "0.4.0-aether-mvp",
        "core": "objective -> requirements -> case -> parallel work graph -> execution -> human authority -> outcome",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "aether_core": "ready"}


@app.get("/ready")
async def readiness_check():
    from backend.database import engine
    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return {"status": "ready", "database": "ready", "aether_core": "ready"}
    except Exception as exc:
        logger.warning("Aether readiness check failed: %s", type(exc).__name__)
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "database": "unavailable",
                "aether_core": "ready",
                "error": type(exc).__name__,
            },
        )
