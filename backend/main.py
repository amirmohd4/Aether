from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import database and models
from database import init_db, engine
from models.database_models import Base
from .database import init_db, engine
from .models.database_models import Base
from api.property_routes import router as property_router
from .api.property_routes import router as property_router
from .api.workflow_routes import router as workflow_router
from .api.fraud_routes import router as fraud_router
from .api.certificate_routes import router as certificate_router
from .api.system_routes import router as system_router
from .api.land_ecosystem_routes import router as land_ecosystem_router
# Import services
rom .services import fraud_service
from .database import SessionLocal

# Initialize FastAPI app
app = FastAPI(
    title="Aether GovOS API",
    description="Government Integration Operating System - Unified API for property and certificate services",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    logger.info("🚀 Starting Aether GovOS...")
    
    try:
        # Initialize database
        logger.info("📊 Initializing database...")
        init_db()
        logger.info("✅ Database initialized")
        
        # Train fraud detection model
        logger.info("🤖 Training fraud detection model...")
        db = SessionLocal()
        try:
            fraud_service.train_model(db)
            logger.info("✅ Fraud detection model trained")
        finally:
            db.close()
        
        logger.info("✅ Aether GovOS started successfully")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Aether GovOS",
        "version": "1.0.0",
        "description": "Government Integration Operating System",
        "tagline": "One API for all government services",
        "documentation": "/api/docs",
        "health": "/api/system/health",
        "marketplace": "/api/system/api-marketplace"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "healthy", "service": "Aether GovOS"}

# Include API routers
app.include_router(property_router, prefix="/api")
app.include_router(workflow_router, prefix="/api")
app.include_router(fraud_router, prefix="/api")
app.include_router(certificate_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(land_ecosystem_router, prefix="/api")

# Error handler for 404
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested resource was not found: {request.url.path}",
            "documentation": "/api/docs"
        }
    )

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "detail": str(exc) if app.debug else None
        }
    )

# Middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
