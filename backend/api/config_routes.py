from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from backend.config_loader import config_loader

router = APIRouter(prefix="/api/v1/config", tags=["Country Configuration"])

@router.get("/countries")
def get_countries():
    """Get list of all supported countries in Aether."""
    return {"status": "success", "countries": config_loader.list_available_countries()}

@router.get("/country/{country_code}")
def get_country_config(country_code: str):
    """Get complete country configuration rules, departments, services, and currency."""
    config = config_loader.get_country_config(country_code)
    if not config:
        raise HTTPException(status_code=404, detail=f"Country configuration '{country_code}' not found")
    return {"status": "success", "config": config}

@router.get("/country/{country_code}/departments")
def get_departments(country_code: str):
    """Get list of departments for selected country."""
    departments = config_loader.get_country_departments(country_code)
    return {"status": "success", "country": country_code, "departments": departments}

@router.get("/country/{country_code}/services")
def get_services(country_code: str, department_id: Optional[str] = None):
    """Get service catalog for country with optional department filtering."""
    services = config_loader.get_country_services(country_code)
    if department_id:
        services = [s for s in services if s.get("department_id") == department_id]
    return {"status": "success", "country": country_code, "count": len(services), "services": services}

@router.get("/country/{country_code}/states")
def get_states(country_code: str):
    """Get list of states/regions/provinces for selected country."""
    states = config_loader.get_country_states(country_code)
    return {"status": "success", "country": country_code, "count": len(states), "states": states}

