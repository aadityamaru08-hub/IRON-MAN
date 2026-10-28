from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from backend.app.db.sqlite_db import db_get_leads, db_get_lead

router = APIRouter(tags=["Leads"])

@router.get("/leads")
def list_leads(status: Optional[str] = Query(None, description="Filter by status (NEW, QUALIFIED, UNQUALIFIED, CONTACTED)")):
    """Retrieve leads from the SQLite database."""
    return db_get_leads(status=status)

@router.get("/leads/{lead_id}")
def get_lead(lead_id: str):
    """Retrieve a single lead record from SQLite by ID."""
    lead = db_get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
