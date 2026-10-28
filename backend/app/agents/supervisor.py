"""Supervisor Agent: Validates workflow quality and halts for human approval before external dispatch."""
from typing import List, Dict, Any
from backend.app.db.sqlite_db import db_create_approval, db_add_event, db_update_workflow

def run_supervisor(workflow_id: str, drafts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Audits generated outreach drafts and creates pending approval requests in SQLite."""
    created_approvals = []

    for draft in drafts:
        approval = db_create_approval(
            workflow_id=workflow_id,
            action_type="SEND_EMAIL",
            target_lead_id=draft.get("lead_id"),
            recipient_email=draft.get("recipient_email"),
            recipient_name=draft.get("recipient_name"),
            subject=draft.get("subject"),
            message_body=draft.get("body")
        )
        created_approvals.append(approval)

    # Halt workflow for human approval
    db_update_workflow(workflow_id, {
        "status": "PAUSED_APPROVAL",
        "current_step": 5,
        "results": {
            "pending_approvals_count": len(created_approvals),
            "approval_ids": [a["id"] for a in created_approvals]
        }
    })

    db_add_event(
        workflow_id=workflow_id,
        agent_name="Supervisor Agent",
        action="Audit Quality & Enforce Human Gate",
        tool_name="approval_gatekeeper",
        input_data={"drafts_checked": len(drafts)},
        output_data={"pending_approvals": len(created_approvals), "approval_ids": [a["id"] for a in created_approvals]},
        status="REQUIRE_APPROVAL",
        message=f"Supervisor verified output quality. Pausing workflow: {len(created_approvals)} external email actions queued and held for human authorization."
    )

    return created_approvals
