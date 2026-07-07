from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import Property

router = APIRouter(prefix="/plan-scrutiny", tags=["Plan Scrutiny"])

@router.post("/scrutinize")
async def scrutinize_plan(data: dict, db: Session = Depends(get_db)):
    """
    AI plan scrutiny: Check building plan against zoning, fire safety, structural rules.
    Simulated rule‑based checks.
    """
    property_id = data.get("property_id")
    plan_details = data.get("plan_details", {})
    if not property_id:
        raise HTTPException(status_code=400, detail="property_id required")
    
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Rule‑based scrutiny
    issues = []
    warnings = []
    
    # 1. Check floor area ratio (FAR) – simplified
    plot_area = prop.property_size
    built_up_area = plan_details.get("built_up_area", 0)
    if built_up_area / plot_area > 2.5:
        issues.append("FAR exceeds permissible limit of 2.5")
    
    # 2. Check building height
    height = plan_details.get("height", 0)
    if height > 15:
        warnings.append("Building height > 15m – requires Fire NOC")
    
    # 3. Check set-back norms
    setback = plan_details.get("setback", 0)
    if setback < 3:
        warnings.append("Setback less than 3m – may require relaxation")
    
    # 4. Check parking provision
    parking = plan_details.get("parking", 0)
    if parking < 1:
        issues.append("Parking provision insufficient")
    
    score = max(0, 100 - len(issues) * 20 - len(warnings) * 5)
    if score < 50:
        status = "rejected"
    elif score < 80:
        status = "conditional_approval"
    else:
        status = "approved"
    
    return {
        "property_id": property_id,
        "scrutiny_status": status,
        "score": score,
        "issues": issues,
        "warnings": warnings,
        "recommendations": [
            "Rectify FAR before resubmission" if "FAR" in " ".join(issues) else None,
            "Ensure Fire NOC compliance" if "15m" in " ".join(warnings) else None
        ],
        "next_steps": "Submit revised plan" if issues else "Proceed to NOC collection"
    }
