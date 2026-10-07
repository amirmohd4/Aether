import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)


# Read DATABASE_URL from the environment. Render/Supabase use PostgreSQL;
# local development and CI may use SQLite.
raw_database_url = os.getenv("DATABASE_URL")
if not raw_database_url:
    if os.getenv("AETHER_ENV", "development").strip().lower() == "production":
        raise RuntimeError("DATABASE_URL is required in production")
    raw_database_url = "sqlite:///./aether.db"

DATABASE_URL = raw_database_url
_database_url = make_url(DATABASE_URL)

# Render can retain a stale Supabase database URL. Correct endpoint components
# from deployment settings and support dedicated Aether database credentials.
if _database_url.get_backend_name() != "sqlite":
    updates = {}

    host_override = os.getenv("AETHER_DATABASE_HOST_OVERRIDE", "").strip()
    if host_override:
        updates["host"] = host_override

    password_override = os.getenv("AETHER_DATABASE_PASSWORD", "")
    if password_override:
        updates["password"] = password_override

    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    project_ref = ""
    if ".supabase.co" in supabase_url:
        project_ref = supabase_url.split("//", 1)[-1].split(".", 1)[0]

    pooler_host = host_override or _database_url.host or ""
    if project_ref and ".pooler.supabase.com" in pooler_host:
        role_override = os.getenv("AETHER_DATABASE_ROLE_OVERRIDE", "").strip()
        if role_override:
            # Shared pooler identities are <ROLE>.<PROJECT-REF>.
            updates["username"] = f"{role_override}.{project_ref}"
        elif not _database_url.username or _database_url.username == "postgres":
            # Default PostgreSQL role over the shared pooler uses the project ref.
            updates["username"] = f"postgres.{project_ref}"

    if updates:
        _database_url = _database_url.set(**updates)
        DATABASE_URL = _database_url.render_as_string(hide_password=False)

    logger.info(
        "Aether database endpoint configured: host=%s port=%s user=%s password_override=%s",
        _database_url.host,
        _database_url.port,
        _database_url.username,
        bool(password_override),
    )


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
