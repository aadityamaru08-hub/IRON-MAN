"""CRM Agent Tools: Interacting directly with SQLite leads database."""
from typing import Dict, Any, List, Optional
from backend.app.db.sqlite_db import db_get_leads, db_get_lead, db_update_lead, db_add_event

def crm_fetch_leads(workflow_id: Optional[str] = None, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches leads from SQLite CRM database and logs the execution."""
    leads = db_get_leads(status=status_filter)
    db_add_event(
        workflow_id=workflow_id,
        agent_name="CRM Agent",
        action="Fetch CRM Leads",
        tool_name="crm_fetch_leads",
        input_data={"status_filter": status_filter},
        output_data={"retrieved_count": len(leads)},
        status="SUCCESS",
        message=f"Retrieved {len(leads)} lead records from SQLite CRM database."
    )
    return leads

def crm_update_lead_record(
    workflow_id: Optional[str],
    lead_id: str,
    score: int,
    status: str,
    priority: str,
    notes: str
) -> Optional[Dict[str, Any]]:
    """Updates a lead record in SQLite and logs the tool execution."""
    updates = {
        "score": score,
        "status": status,
        "priority": priority,
        "notes": notes
    }
    updated = db_update_lead(lead_id, updates)
    if not updated:
        db_add_event(
            workflow_id=workflow_id,
            agent_name="CRM Agent",
            action="Update Lead Record (Failed)",
            tool_name="crm_update_lead_record",
            input_data={"lead_id": lead_id, "updates": updates},
            status="ERROR",
            message=f"Failed to update lead {lead_id}: Record not found."
        )
        return None

    db_add_event(
        workflow_id=workflow_id,
        agent_name="CRM Agent",
        action="Update Lead Record",
        tool_name="crm_update_lead_record",
        input_data={"lead_id": lead_id, "score": score, "status": status, "priority": priority},
        output_data={"lead_id": lead_id, "company": updated.get("company"), "new_status": status, "score": score},
        status="SUCCESS",
        message=f"Updated CRM record for {updated.get('name')} ({updated.get('company')}) - Score: {score}/100, Status: {status}, Priority: {priority}."
    )
    return updated
