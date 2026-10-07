import os

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Read DATABASE_URL from the environment. Render/Supabase use PostgreSQL;
# local development and CI may use SQLite.
raw_database_url = os.getenv("DATABASE_URL")
if not raw_database_url:
    if os.getenv("AETHER_ENV", "development").strip().lower() == "production":
        raise RuntimeError("DATABASE_URL is required in production")
    raw_database_url = "sqlite:///./aether.db"

DATABASE_URL = raw_database_url
_database_url = make_url(DATABASE_URL)


if _database_url.get_backend_name() == "sqlite":
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    # Connection-specific options such as connect_timeout belong to
    # PostgreSQL-style DBAPI drivers, not SQLite.
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5},
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
