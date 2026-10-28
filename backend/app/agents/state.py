from typing import List, Dict, Any, Optional, Annotated
from typing_extensions import TypedDict
import operator

class AgentState(TypedDict):
    """LangGraph multi-agent shared execution state."""
    request: str
    plan: List[str]
    current_step: int
    leads: List[Dict[str, Any]]
    qualified_leads: List[Dict[str, Any]]
    crm_updates: List[Dict[str, Any]]
    outreach_drafts: List[Dict[str, Any]]
    requires_approval: bool
    approval_details: Optional[Dict[str, Any]]
    approved: bool
    results: Dict[str, Any]
    status: str
    logs: Annotated[List[Dict[str, Any]], operator.add]
