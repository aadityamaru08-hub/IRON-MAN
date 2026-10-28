from fastapi import APIRouter
from backend.app.config import settings
from backend.app.db.sqlite_db import db_get_leads

router = APIRouter(tags=["Health"])

@router.get("/health")
def get_health():
    """Health check endpoint to verify backend connectivity, SQLite DB status, and AI config."""
    leads = db_get_leads()
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.version,
        "database": "sqlite",
        "has_anthropic_key": settings.has_anthropic_key,
        "llm_engine": "Claude 3.5 Sonnet" if settings.has_anthropic_key else "Deterministic Rule-Based Fallback",
        "leads_count": len(leads)
    }
