from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/aether_govos")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import all models so Base.metadata.create_all picks them up
import models.database_models  # noqa: F401
import models.trade_license  # noqa: F401
import models.building_permit  # noqa: F401
import models.water_connection  # noqa: F401
import models.birth_certificate  # noqa: F401
import models.death_certificate  # noqa: F401
import models.medical_license  # noqa: F401
import models.admission  # noqa: F401
import models.transfer_certificate  # noqa: F401
import models.factory_license  # noqa: F401
import models.pf_esi  # noqa: F401
import models.gst_registration  # noqa: F401
import models.company_registration  # noqa: F401
import models.ration_card  # noqa: F401
import models.pds_subsidy  # noqa: F401
import models.police_clearance  # noqa: F401
import models.fir_report  # noqa: F401
import models.farmer_id  # noqa: F401
import models.crop_insurance  # noqa: F401
import models.pmay_application  # noqa: F401
import models.affordable_housing  # noqa: F401
import models.rera_project  # noqa: F401
import models.rera_certificate  # noqa: F401
import models.court_case_filing  # noqa: F401
import models.e_court  # noqa: F401
import models.passport_application  # noqa: F401
import models.visa_service  # noqa: F401


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
