from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use SQLite for development (change this to your actual DB URL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./aether.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# You can import your models here to create tables
# from backend.models.database_models import Property, WorkflowState, FraudDetectionLog

# Uncomment to create tables on startup (optional)
# Base.metadata.create_all(bind=engine)
