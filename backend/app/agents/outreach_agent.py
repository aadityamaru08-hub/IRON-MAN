"""Outreach Agent: Generates personalized messages for qualified leads."""
from typing import List, Dict, Any
from backend.app.config import settings
from backend.app.db.sqlite_db import db_add_event

def generate_deterministic_message(lead: Dict[str, Any]) -> Dict[str, str]:
    """Generates personalized follow-up email draft deterministically."""
    name = lead.get("name", "Prospect")
    company = lead.get("company", "Your Company")
    requirement = lead.get("requirement", "business automation")
    urgency = str(lead.get("urgency", "High")).lower()

    subject = f"Accelerating {requirement[:40]}... for {company}"
    body = (
        f"Hi {name},\n\n"
        f"I reviewed your initiative at {company} regarding {requirement}. "
        f"Given your {urgency} timeline, BizForce AI's multi-agent orchestration "
        f"can automate this end-to-end with full compliance and real-time oversight.\n\n"
        f"We've prepared an initial solution blueprint for {company}. "
        f"Would you be open to a 15-minute walkthrough this week?\n\n"
        f"Best regards,\n"
        f"BizForce AI Autonomous Outreach Engine"
    )
    return {"subject": subject, "body": body}

def run_outreach_agent(workflow_id: str, qualified_leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Synthesizes bespoke outreach drafts for qualified prospects."""
    has_llm = settings.has_anthropic_key
    drafts = []

    # Target top qualified leads
    leads_to_contact = [l for l in qualified_leads if l.get("status") == "QUALIFIED"]
    if not leads_to_contact:
        leads_to_contact = qualified_leads[:3]  # fallback to top scored

    for lead in leads_to_contact:
        llm_used = False
        fallback = generate_deterministic_message(lead)
        subject = fallback["subject"]
        body = fallback["body"]

        if has_llm:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
                prompt = f"""Write a professional, personalized follow-up sales email to:
Contact: {lead.get('name')}
Company: {lead.get('company')}
Requirement: {lead.get('requirement')}
Budget: ${lead.get('budget')}
Urgency: {lead.get('urgency')}

Format response as:
SUBJECT: <subject line>
BODY:
<email body>"""
                resp = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                text = resp.content[0].text.strip()
                if "SUBJECT:" in text and "BODY:" in text:
                    parts = text.split("BODY:")
                    subject = parts[0].replace("SUBJECT:", "").strip()
                    body = parts[1].strip()
                    llm_used = True
            except Exception:
                llm_used = False

        drafts.append({
            "lead_id": lead["id"],
            "recipient_name": lead.get("name"),
            "recipient_email": lead.get("email"),
            "company": lead.get("company"),
            "subject": subject,
            "body": body,
            "llm_used": llm_used
        })

    log_msg = (
        f"Claude API generated {len(drafts)} personalized outreach message drafts."
        if any(d["llm_used"] for d in drafts) else
        f"LLM not configured; generated deterministic rule-based personalized outreach for {len(drafts)} prospects."
    )

    db_add_event(
        workflow_id=workflow_id,
        agent_name="Outreach Agent",
        action="Generate Outreach Drafts",
        tool_name="tool_draft_outreach_message",
        input_data={"qualified_leads_count": len(leads_to_contact)},
        output_data={"drafts_count": len(drafts), "sample": drafts[0] if drafts else None},
        status="SUCCESS",
        message=log_msg
    )

    return drafts
