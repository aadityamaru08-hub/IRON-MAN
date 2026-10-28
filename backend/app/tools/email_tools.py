"""Mock Email Tool: Records approved email outreach dispatches directly in SQLite."""
from typing import Dict, Any, Optional
from backend.app.db.sqlite_db import db_record_sent_message, db_update_lead, db_add_event

def tool_mock_send_email(
    workflow_id: str,
    approval_id: str,
    lead_id: str,
    recipient: str,
    subject: str,
    body: str
) -> Dict[str, Any]:
    """Records dispatched email in SQLite sent_messages table. Never sends real emails."""
    # 1. Record in SQLite sent_messages table
    record = db_record_sent_message(
        approval_id=approval_id,
        workflow_id=workflow_id,
        lead_id=lead_id,
        recipient=recipient,
        subject=subject,
        body=body
    )

    # 2. Update CRM status to CONTACTED
    if lead_id:
        db_update_lead(lead_id, {"status": "CONTACTED"})

    # 3. Log event
    db_add_event(
        workflow_id=workflow_id,
        agent_name="Mock Email Tool",
        action="Dispatch Approved Outreach Email",
        tool_name="tool_mock_send_email",
        input_data={"approval_id": approval_id, "recipient": recipient, "subject": subject},
        output_data=record,
        status="SUCCESS",
        message=f"Dispatched email to {recipient} (Recorded in SQLite sent_messages table. No real email transmitted)."
    )

    return record
