"""BizForce AI Multi-Agent Workflow Engine."""
from typing import Dict, Any, List
from backend.app.db.sqlite_db import (
    db_create_workflow, db_get_workflow, db_update_workflow,
    db_get_leads, db_add_event
)
from backend.app.agents.orchestrator import run_orchestrator
from backend.app.agents.lead_agent import run_lead_qualification
from backend.app.agents.crm_agent import run_crm_agent
from backend.app.agents.outreach_agent import run_outreach_agent
from backend.app.agents.supervisor import run_supervisor

def execute_business_workflow(request_text: str) -> Dict[str, Any]:
    """Executes the complete multi-agent workflow sequentially with persistent SQLite logging."""
    # 1. Initialize workflow record
    initial_plan = [
        "1. Orchestrator parses business request and creates execution plan",
        "2. Lead Qualification Agent scores leads based on budget, urgency, and requirement fit (0-100)",
        "3. CRM Agent updates SQLite records with qualification scores, status, and priorities",
        "4. Outreach Agent synthesizes personalized follow-up messages for qualified prospects",
        "5. Supervisor Agent audits generated actions and halts at Human-in-the-Loop gate before dispatch"
    ]
    wf = db_create_workflow(request_text, initial_plan)
    workflow_id = wf["id"]

    try:
        # Step 1: Orchestrator
        db_update_workflow(workflow_id, {"current_step": 1, "status": "RUNNING"})
        refined_plan = run_orchestrator(workflow_id, request_text)
        db_update_workflow(workflow_id, {"plan": refined_plan})

        # Step 2: Retrieve leads & run Lead Qualification Agent
        db_update_workflow(workflow_id, {"current_step": 2})
        leads = db_get_leads()
        evaluations = run_lead_qualification(workflow_id, leads)

        # Step 3: CRM Agent updates SQLite records
        db_update_workflow(workflow_id, {"current_step": 3})
        updated_records = run_crm_agent(workflow_id, evaluations)

        # Step 4: Outreach Agent drafts personalized emails
        db_update_workflow(workflow_id, {"current_step": 4})
        drafts = run_outreach_agent(workflow_id, updated_records)

        # Step 5: Supervisor audits and halts for human approval
        db_update_workflow(workflow_id, {"current_step": 5})
        approvals = run_supervisor(workflow_id, drafts)

        # Retrieve final workflow state
        final_wf = db_get_workflow(workflow_id)
        return final_wf

    except Exception as e:
        error_msg = f"Workflow encountered an error: {str(e)}"
        db_update_workflow(workflow_id, {"status": "FAILED", "results": {"error": str(e)}})
        db_add_event(
            workflow_id=workflow_id,
            agent_name="System",
            action="Workflow Error",
            status="ERROR",
            message=error_msg
        )
        return db_get_workflow(workflow_id)
