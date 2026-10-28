"""Lead Qualification Agent: Evaluates leads using budget, requirement, and urgency (0-100 score)."""
from typing import List, Dict, Any, Tuple
from backend.app.config import settings
from backend.app.db.sqlite_db import db_add_event

HIGH_INTENT_KEYWORDS = [
    "automation", "orchestration", "dispatch", "telemetry", "compliance",
    "hipaa", "kyc", "regulatory", "predictive", "rfq", "concierge", "robotics"
]

def calculate_deterministic_score(lead: Dict[str, Any]) -> Tuple[int, str, str, str]:
    """Deterministic lead scoring algorithm based on budget, urgency, and requirement."""
    budget = float(lead.get("budget", 0))
    urgency = str(lead.get("urgency", "MEDIUM")).upper()
    requirement = str(lead.get("requirement", "")).lower()

    # 1. Budget Score (0-40 pts)
    if budget >= 120000:
        budget_score = 40
    elif budget >= 90000:
        budget_score = 35
    elif budget >= 65000:
        budget_score = 30
    elif budget >= 40000:
        budget_score = 22
    elif budget >= 25000:
        budget_score = 14
    else:
        budget_score = 8

    # 2. Urgency Score (0-35 pts)
    if urgency == "CRITICAL":
        urgency_score = 35
    elif urgency == "HIGH":
        urgency_score = 28
    elif urgency == "MEDIUM":
        urgency_score = 18
    else:
        urgency_score = 8

    # 3. Requirement Fit (0-25 pts)
    matches = sum(1 for kw in HIGH_INTENT_KEYWORDS if kw in requirement)
    if matches >= 3:
        fit_score = 25
    elif matches == 2:
        fit_score = 20
    elif matches == 1:
        fit_score = 15
    else:
        fit_score = 10

    total_score = min(100, max(0, budget_score + urgency_score + fit_score))

    if total_score >= 65:
        status = "QUALIFIED"
        priority = "HIGH"
    elif total_score >= 45:
        status = "QUALIFIED"
        priority = "MEDIUM"
    else:
        status = "UNQUALIFIED"
        priority = "LOW"

    rationale = f"Evaluated Budget (${budget:,.0f} -> {budget_score}pts), Urgency ({urgency} -> {urgency_score}pts), Fit ({matches} core keywords -> {fit_score}pts)."
    return total_score, status, priority, rationale

def run_lead_qualification(workflow_id: str, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Evaluates all leads and returns structured qualification results."""
    has_llm = settings.has_anthropic_key
    evaluated_leads = []

    for lead in leads:
        llm_used = False
        score, status, priority, rationale = calculate_deterministic_score(lead)

        if has_llm:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
                prompt = f"""Evaluate this sales lead:
Company: {lead.get('company')}
Contact: {lead.get('name')}
Budget: ${lead.get('budget')}
Urgency: {lead.get('urgency')}
Requirement: {lead.get('requirement')}

Respond in JSON format:
{{"score": <integer 0-100>, "status": "<QUALIFIED or UNQUALIFIED>", "priority": "<HIGH, MEDIUM, or LOW>", "rationale": "<one concise sentence>"}}"""
                resp = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=150,
                    messages=[{"role": "user", "content": prompt}]
                )
                import json
                parsed = json.loads(resp.content[0].text.strip())
                score = int(parsed.get("score", score))
                status = str(parsed.get("status", status)).upper()
                priority = str(parsed.get("priority", priority)).upper()
                rationale = parsed.get("rationale", rationale)
                llm_used = True
            except Exception:
                llm_used = False

        evaluated_leads.append({
            "lead_id": lead["id"],
            "name": lead.get("name"),
            "company": lead.get("company"),
            "score": score,
            "status": status,
            "priority": priority,
            "notes": rationale,
            "llm_used": llm_used
        })

    qualified_count = sum(1 for l in evaluated_leads if l["status"] == "QUALIFIED")
    log_msg = (
        f"Claude API analyzed {len(leads)} leads: {qualified_count} marked QUALIFIED."
        if any(l["llm_used"] for l in evaluated_leads) else
        f"LLM not configured; executed deterministic rule-based qualification algorithm on {len(leads)} leads: {qualified_count} marked QUALIFIED."
    )

    db_add_event(
        workflow_id=workflow_id,
        agent_name="Lead Qualification Agent",
        action="Evaluate Leads",
        tool_name="tool_evaluate_lead",
        input_data={"leads_evaluated": len(leads)},
        output_data={"qualified_count": qualified_count, "results": evaluated_leads[:3]},
        status="SUCCESS",
        message=log_msg
    )

    return evaluated_leads
