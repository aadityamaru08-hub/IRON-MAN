from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.app.db.sqlite_db import db_get_workflow, db_get_events
from backend.app.agents.graph import execute_business_workflow

router = APIRouter(tags=["Workflows"])

class WorkflowRequest(BaseModel):
    request: str

@router.post("/workflows/run")
def start_workflow(payload: WorkflowRequest):
    """Executes multi-agent workflow: Orchestrator -> Qualification -> CRM -> Outreach -> Supervisor."""
    if not payload.request.strip():
        raise HTTPException(status_code=400, detail="Request text cannot be empty")
    result = execute_business_workflow(payload.request.strip())
    return result

# Static paths must be defined before parameterized path {workflow_id}
@router.get("/workflows/logs")
@router.get("/workflows/events")
def get_workflow_events(
    workflow_id: Optional[str] = Query(None, description="Optional filter by workflow ID"),
    limit: int = Query(50, description="Max number of logs to return")
):
    """Retrieve real-time agent execution events and tool logs from SQLite."""
    return db_get_events(workflow_id=workflow_id, limit=limit)

@router.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    """Retrieve the current state of a workflow execution from SQLite."""
    wf = db_get_workflow(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return wf
