from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.mutation_service import mutation_service
from services.ec_service import ec_service
from services.land_conversion_service import land_conversion_service
from services.title_verification_service import title_service
from pydantic import BaseModel

router = APIRouter(prefix="/workflow", tags=["Land Ecosystem Workflows"])

# ============= MUTATION WORKFLOW =============

class MutationStartRequest(BaseModel):
    property_id: str
    new_owner: str
    transfer_type: str = "Sale"

@router.post("/mutation/start")
async def start_mutation(request: MutationStartRequest, db: Session = Depends(get_db)):
    """Start mutation workflow"""
    try:
        result = mutation_service.start_mutation(
            db=db,
            property_id=request.property_id,
            new_owner=request.new_owner,
            transfer_type=request.transfer_type
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mutation/{mutation_id}/status")
async def get_mutation_status(mutation_id: str, db: Session = Depends(get_db)):
    """Get mutation workflow status"""
    try:
        result = mutation_service.get_status(db, mutation_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============= ENCUMBRANCE CERTIFICATE WORKFLOW =============

class ECGenerateRequest(BaseModel):
    property_id: str
    years: int = 30

@router.post("/ec/generate")
async def generate_ec(request: ECGenerateRequest, db: Session = Depends(get_db)):
    """Generate Encumbrance Certificate"""
    try:
        result = ec_service.generate_ec(db=db, property_id=request.property_id, years=request.years)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ec/{ec_id}")
async def get_ec(ec_id: str, db: Session = Depends(get_db)):
    """Get Encumbrance Certificate by ID"""
    try:
        result = ec_service.get_ec(db, ec_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ec/property/{property_id}/history")
async def get_ec_history(property_id: str, db: Session = Depends(get_db)):
    """Get all ECs for a property"""
    try:
        result = ec_service.get_ec_history(db, property_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============= LAND USE CONVERSION WORKFLOW =============

class ConversionStartRequest(BaseModel):
    property_id: str
    target_use: str  # residential, commercial, industrial, agricultural

@router.post("/conversion/start")
async def start_land_conversion(request: ConversionStartRequest, db: Session = Depends(get_db)):
    """Start land use conversion workflow"""
    try:
        result = land_conversion_service.start_conversion(
            db=db,
            property_id=request.property_id,
            target_use=request.target_use
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversion/{conversion_id}/status")
async def get_conversion_status(conversion_id: str, db: Session = Depends(get_db)):
    """Get land conversion workflow status"""
    try:
        result = land_conversion_service.get_status(db, conversion_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============= TITLE VERIFICATION WORKFLOW =============

class TitleVerifyRequest(BaseModel):
    property_id: str
    owner_aadhaar: str = None

@router.post("/title/verify")
async def verify_title(request: TitleVerifyRequest, db: Session = Depends(get_db)):
    """Verify property title"""
    try:
        result = title_service.verify_title(
            db=db,
            property_id=request.property_id,
            owner_aadhaar=request.owner_aadhaar
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/title/{verification_id}")
async def get_title_verification(verification_id: str, db: Session = Depends(get_db)):
    """Get title verification by ID"""
    try:
        result = title_service.get_verification(db, verification_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
