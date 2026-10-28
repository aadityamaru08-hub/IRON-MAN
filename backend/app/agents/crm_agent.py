"""CRM Agent: Updates SQLite database records using actual Python functions."""
from typing import List, Dict, Any
from backend.app.tools.crm_tools import crm_update_lead_record
from backend.app.db.sqlite_db import db_add_event

def run_crm_agent(workflow_id: str, evaluations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Iterates through qualified/evaluated leads and commits updates to SQLite CRM database."""
    updated_records = []

    for ev in evaluations:
        updated = crm_update_lead_record(
            workflow_id=workflow_id,
            lead_id=ev["lead_id"],
            score=ev["score"],
            status=ev["status"],
            priority=ev["priority"],
            notes=ev["notes"]
        )
        if updated:
            updated_records.append(updated)

    db_add_event(
        workflow_id=workflow_id,
        agent_name="CRM Agent",
        action="Batch CRM Sync",
        tool_name="crm_update_lead_record",
        input_data={"records_to_sync": len(evaluations)},
        output_data={"records_updated": len(updated_records)},
        status="SUCCESS",
        message=f"CRM Agent committed {len(updated_records)} lead updates to SQLite database via python functions."
    )

    return updated_records
