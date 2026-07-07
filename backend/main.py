from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import sys
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import database and models (absolute imports – no dots)
from database import init_db, SessionLocal
from models.database_models import Base

# Import API routes (absolute imports)
from api.property_routes import router as property_router
from api.workflow_routes import router as workflow_router
from api.fraud_routes import router as fraud_router
from api.certificate_routes import router as certificate_router
from api.system_routes import router as system_router
from api.land_ecosystem_routes import router as land_ecosystem_router
from api.bank_routes import router as bank_router
from api.developer_routes import router as developer_router
from api.officer_routes import router as officer_router
# Import services
from services import fraud_service

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
                # Check if database has any properties
        from database import SessionLocal
        from models.database_models import Property
        db = SessionLocal()
        property_count = db.query(Property).count()
        db.close()
        
        if property_count == 0:
            logger.info("📦 Database empty. Seeding mock data...")
            import subprocess, sys
            python_path = sys.executable
            result = subprocess.run([python_path, "scripts/generate_mock_data.py"], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ Mock data seeded successfully")
            else:
                logger.error(f"❌ Seeding failed: {result.stderr}")
        else:
            logger.info(f"📊 Database already contains {property_count} properties. Skipping seed.")
        # Train fraud detection model
        logger.info("🤖 Training fraud detection model...")
        try:
            fraud_service.train_model(SessionLocal())
            logger.info("✅ Fraud detection model trained")
        except Exception as e:
            logger.warning(f"Fraud model training skipped: {e}")
        
        logger.info("✅ Aether GovOS started successfully")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

# Root endpoint
@app.get("/")
async def root():
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
    return {"status": "healthy", "service": "Aether GovOS"}
@app.get("/admin/seed")
async def seed_database():
    """Generate mock data directly using the database session (no subprocess)."""
    from database import SessionLocal
    from models.database_models import Property, Citizen
    import random
    from faker import Faker
    from datetime import datetime, timedelta
    import uuid

    fake = Faker('en_IN')

    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Property).count() > 0:
            return {"status": "already_seeded", "count": db.query(Property).count()}

        # Generate 100 citizens
        citizens = []
        for _ in range(100):
            citizen = Citizen(
                citizen_id=f"CIT-{uuid.uuid4().hex[:8].upper()}",
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number()[:15],
                aadhaar_number=f"{random.randint(100000000000, 999999999999)}",
                verified_attributes={
                    "aadhaar_verified": random.choice([True, False]),
                    "phone_verified": random.choice([True, False]),
                    "email_verified": random.choice([True, False])
                },
                state=random.choice(["karnataka", "jk"]),
                district=random.choice(["Bengaluru Urban", "Srinagar"]),
                address=fake.address()
            )
            citizens.append(citizen)
        db.bulk_save_objects(citizens)
        db.commit()

        # Generate 1000 properties (enough for demo)
        properties = []
        for i in range(1000):
            prop_id = f"KAR-PROP-{i:04d}" if i < 500 else f"JK-PROP-{i-500:04d}"
            state = "karnataka" if i < 500 else "jk"
            prop = Property(
                property_id=prop_id,
                state=state,
                location=fake.address(),
                district=random.choice(["Bengaluru Urban", "Mysuru", "Srinagar", "Jammu"]),
                tehsil=random.choice(["North", "South", "East", "West"]),
                village=fake.city(),
                owner=fake.name(),
                owner_citizen_id=random.choice(citizens).citizen_id,
                title_status=random.choice(["clear", "clear", "clear", "disputed"]),  # 75% clear
                encumbrances=[{"type": "mortgage", "amount": random.uniform(100000, 5000000)}] if random.random() < 0.1 else [],
                history=[{"date": (datetime.now() - timedelta(days=random.randint(365, 3650))).isoformat(),
                          "transaction_type": random.choice(["sale", "inheritance"]),
                          "previous_owner": fake.name()} for _ in range(random.randint(1, 3))],
                property_value=random.uniform(500000, 50000000),
                property_size=random.uniform(500, 5000),
                property_type=random.choice(["residential", "commercial", "agricultural"]),
                state_specific_data={"fraud_flags": {}}
            )
            properties.append(prop)
        db.bulk_save_objects(properties)
        db.commit()

        return {"status": "success", "message": f"Seeded {len(properties)} properties and {len(citizens)} citizens."}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
# Include API routers
app.include_router(property_router, prefix="/api")
app.include_router(workflow_router, prefix="/api")
app.include_router(fraud_router, prefix="/api")
app.include_router(certificate_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(land_ecosystem_router, prefix="/api")
app.include_router(bank_router)
app.include_router(developer_router)
app.include_router(officer_router)
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
# ============================================================
# SERVE REACT FRONTEND FROM BACKEND
# ============================================================


frontend_dist = Path(__file__).parent.parent / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
# ============================================================
