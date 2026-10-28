from backend.app.tools.crm_tools import crm_fetch_leads, crm_update_lead_record
from backend.app.tools.email_tools import tool_mock_send_email

# Aliases for compatibility
tool_get_leads = crm_fetch_leads
tool_update_lead = crm_update_lead_record

__all__ = [
    "crm_fetch_leads",
    "crm_update_lead_record",
    "tool_mock_send_email",
    "tool_get_leads",
    "tool_update_lead"
]
