"""Orchestrator Agent: Receives business request, formulates visible task plan."""
from typing import List, Dict, Any
from backend.app.config import settings
from backend.app.db.sqlite_db import db_add_event

def run_orchestrator(workflow_id: str, request_text: str) -> List[str]:
    """Generates a visible multi-step task plan for the workflow."""
    has_llm = settings.has_anthropic_key
    llm_source = "Claude 3.5 Sonnet" if has_llm else "Deterministic Engine"

    plan = [
        "1. Orchestrator parses business request and creates execution plan",
        "2. Lead Qualification Agent scores leads based on budget, urgency, and requirement fit (0-100)",
        "3. CRM Agent updates SQLite records with qualification scores, status, and priorities",
        "4. Outreach Agent synthesizes personalized follow-up messages for qualified prospects",
        "5. Supervisor Agent audits generated actions and halts at Human-in-the-Loop gate before dispatch"
    ]

    if has_llm:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
            prompt = f"""You are the BizForce AI Orchestrator Agent.
Given this business automation request:
"{request_text}"

Generate a concise 5-step execution plan for BizForce AI agents (Lead Qualification, CRM, Outreach, Supervisor).
Return ONLY the 5 numbered steps, one per line."""
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            raw_text = response.content[0].text.strip()
            custom_plan = [line.strip() for line in raw_text.split("\n") if line.strip() and line[0].isdigit()]
            if len(custom_plan) >= 3:
                plan = custom_plan
                llm_used = True
            else:
                llm_used = False
        except Exception as e:
            llm_used = False
    else:
        llm_used = False

    log_message = (
        f"Claude API interpreted request: '{request_text}' and synthesized {len(plan)}-stage plan."
        if llm_used else
        f"LLM not configured; generated deterministic orchestrator task plan for: '{request_text}'."
    )

    db_add_event(
        workflow_id=workflow_id,
        agent_name="Orchestrator Agent",
        action="Synthesize Task Plan",
        tool_name="orchestrator_planner",
        input_data={"request": request_text, "llm_used": llm_used, "source": llm_source},
        output_data={"plan": plan},
        status="SUCCESS",
        message=log_message
    )

    return plan
