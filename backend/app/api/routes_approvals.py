from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from backend.app.db.sqlite_db import (
    get_connection, db_get_approval, db_get_approvals,
    db_add_event, db_update_workflow, db_get_workflow
)
from backend.app.tools.email_tools import tool_mock_send_email

router = APIRouter(tags=["Approvals"])

class DecisionPayload(BaseModel):
    comments: Optional[str] = None

@router.get("/approvals")
def list_approvals(
    status: Optional[str] = Query(None, description="Filter by status (PENDING, APPROVED, REJECTED)"),
    workflow_id: Optional[str] = Query(None, description="Filter by workflow ID")
):
    """Retrieve pending or past approval requests."""
    return db_get_approvals(status=status, workflow_id=workflow_id)

@router.post("/approvals/{approval_id}/approve")
def approve_action(approval_id: str, payload: Optional[DecisionPayload] = None):
    """Approve a paused high-impact action and execute it. Idempotent: repeated calls do not duplicate."""
    approval = db_get_approval(approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")

    # Idempotency check: If already approved, return without re-executing
    if approval["status"] == "APPROVED":
        return {
            "message": "Action was already approved and executed (idempotent call).",
            "approval": approval
        }

    if approval["status"] == "REJECTED":
        raise HTTPException(status_code=400, detail="Cannot approve an action that has already been rejected")

    # Atomic update to APPROVED in SQLite
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    comments = payload.comments if payload and payload.comments else ""

    cursor.execute("""
    UPDATE approvals
    SET status = 'APPROVED', decision_at = ?, decision_notes = ?, execution_status = 'EXECUTING'
    WHERE id = ? AND status = 'PENDING'
    """, (now, comments, approval_id))
    conn.commit()
    conn.close()

    # Execute the action (Mock Email Dispatch)
    execution_result = {}
    if approval["action_type"] == "SEND_EMAIL":
        execution_result = tool_mock_send_email(
            workflow_id=approval["workflow_id"],
            approval_id=approval_id,
            lead_id=approval["target_lead_id"],
            recipient=approval["recipient_email"],
            subject=approval["subject"],
            body=approval["message_body"]
        )

    # Update execution status in approvals table
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE approvals
    SET execution_status = 'EXECUTED', execution_result = ?
    WHERE id = ?
    """, (json.dumps(execution_result), approval_id))
    conn.commit()
    conn.close()

    # Check if all approvals for this workflow are resolved; if so mark workflow COMPLETED
    remaining_pending = db_get_approvals(status="PENDING", workflow_id=approval["workflow_id"])
    if len(remaining_pending) == 0:
        db_update_workflow(approval["workflow_id"], {"status": "COMPLETED"})

    db_add_event(
        workflow_id=approval["workflow_id"],
        agent_name="Supervisor Gatekeeper",
        action="Human Approval Granted",
        tool_name="approval_gate",
        input_data={"approval_id": approval_id, "comments": comments},
        output_data=execution_result,
        status="SUCCESS",
        message=f"Human supervisor approved email outreach to {approval['recipient_name']} ({approval['recipient_email']}). Dispatched via mock email tool."
    )

    return {
        "message": "Action successfully approved and executed.",
        "approval": db_get_approval(approval_id)
    }

@router.post("/approvals/{approval_id}/reject")
def reject_action(approval_id: str, payload: Optional[DecisionPayload] = None):
    """Reject a paused high-impact action. Idempotent: repeated calls do not alter rejection."""
    approval = db_get_approval(approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")

    if approval["status"] == "REJECTED":
        return {
            "message": "Action was already rejected (idempotent call).",
            "approval": approval
        }

    if approval["status"] == "APPROVED":
        raise HTTPException(status_code=400, detail="Cannot reject an action that has already been approved and executed")

    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    comments = payload.comments if payload and payload.comments else ""

    cursor.execute("""
    UPDATE approvals
    SET status = 'REJECTED', decision_at = ?, decision_notes = ?, execution_status = 'SKIPPED'
    WHERE id = ? AND status = 'PENDING'
    """, (now, comments, approval_id))
    conn.commit()
    conn.close()

    # If all approvals resolved, update workflow status
    remaining_pending = db_get_approvals(status="PENDING", workflow_id=approval["workflow_id"])
    if len(remaining_pending) == 0:
        db_update_workflow(approval["workflow_id"], {"status": "COMPLETED"})

    db_add_event(
        workflow_id=approval["workflow_id"],
        agent_name="Supervisor Gatekeeper",
        action="Human Action Rejected",
        tool_name="approval_gate",
        input_data={"approval_id": approval_id, "comments": comments},
        status="REJECTED",
        message=f"Human supervisor rejected email outreach to {approval['recipient_name']} ({approval['recipient_email']}). Dispatch aborted."
    )

    return {
        "message": "Action rejected.",
        "approval": db_get_approval(approval_id)
    }
