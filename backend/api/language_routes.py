import os
import json
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/api/v1/languages", tags=["Multi-Language Support (i18n)"])

LANG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "languages")

@router.get("/")
def get_supported_languages():
    """List all supported internationalization languages."""
    languages = []
    if os.path.exists(LANG_DIR):
        for file in os.listdir(LANG_DIR):
            if file.endswith(".json"):
                f_path = os.path.join(LANG_DIR, file)
                try:
                    with open(f_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        languages.append({
                            "code": data.get("lang_code", file.replace(".json", "")),
                            "name": data.get("lang_name", file),
                            "direction": data.get("dir", "ltr")
                        })
                except Exception as e:
                    pass
    return {"status": "success", "languages": languages}

@router.get("/{lang_code}")
def get_language_translations(lang_code: str):
    """Get translation key-value map for the specified language."""
    lang_file = os.path.join(LANG_DIR, f"{lang_code.lower()}.json")
    if not os.path.exists(lang_file):
        # Fallback to English
        lang_file = os.path.join(LANG_DIR, "en.json")
        if not os.path.exists(lang_file):
            raise HTTPException(status_code=404, detail="Language file not found")
            
    with open(lang_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"status": "success", "language": data.get("lang_code"), "translations": data.get("translations", {})}
