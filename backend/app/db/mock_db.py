import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from backend.app.db.base import Lead, AgentLog, WorkflowRun

class MockDatabase:
    """In-memory mock database representing CRM leads, agent execution logs, and workflow runs."""
    
    def __init__(self):
        self.leads: Dict[str, Lead] = {}
        self.logs: List[AgentLog] = []
        self.workflows: Dict[str, WorkflowRun] = {}
        self._seed_initial_data()

    def _seed_initial_data(self):
        seed_leads = [
            Lead(
                id="lead-1",
                name="Sarah Jenkins",
                company="Apex Logistics",
                email="sarah.jenkins@apexlogistics.io",
                title="VP of Operations",
                status="NEW",
                score=45,
                notes="Inquired about warehouse dispatch automation on website form.",
                tags=["Inbound", "SupplyChain", "HighPriority"],
                custom_fields={"fleet_size": 120, "budget_indicated": "$50k-$100k"}
            ),
            Lead(
                id="lead-2",
                name="David Zhang",
                company="Nexus Health",
                email="dzhang@nexushealth.org",
                title="Director of Digital Health",
                status="NEW",
                score=30,
                notes="Downloaded whitepaper on HIPAA-compliant patient intake.",
                tags=["Healthcare", "ContentDownload"],
                custom_fields={"organization_size": "200-500"}
            ),
            Lead(
                id="lead-3",
                name="Elena Rostova",
                company="FinEdge Global",
                email="elena.r@finedge.com",
                title="Head of Customer Experience",
                status="QUALIFIED",
                score=85,
                notes="Urgent need for automated multi-channel client onboarding.",
                tags=["FinTech", "Enterprise", "Urgent"],
                custom_fields={"annual_revenue": "$25M", "timeline": "30 days"}
            ),
            Lead(
                id="lead-4",
                name="Marcus Vance",
                company="Solaria Energy",
                email="m.vance@solariaenergy.com",
                title="Chief Technology Officer",
                status="NEW",
                score=50,
                notes="Requested demo for solar array maintenance ticketing.",
                tags=["CleanTech", "DemoRequest"],
                custom_fields={"inverters_deployed": 1500}
            )
        ]
        for lead in seed_leads:
            self.leads[lead.id] = lead

    def get_leads(self) -> List[Lead]:
        return list(self.leads.values())

    def get_lead(self, lead_id: str) -> Optional[Lead]:
        return self.leads.get(lead_id)

    def update_lead(self, lead_id: str, updates: Dict[str, Any]) -> Optional[Lead]:
        if lead_id not in self.leads:
            return None
        lead = self.leads[lead_id]
        lead_dict = lead.model_dump()
        for k, v in updates.items():
            if k in lead_dict:
                lead_dict[k] = v
        lead_dict["updated_at"] = datetime.utcnow()
        updated_lead = Lead(**lead_dict)
        self.leads[lead_id] = updated_lead
        return updated_lead

    def add_log(self, agent_name: str, action: str, tool_name: Optional[str] = None,
                input_data: Optional[Dict[str, Any]] = None,
                output_data: Optional[Dict[str, Any]] = None,
                status: str = "SUCCESS", message: str = "") -> AgentLog:
        log_entry = AgentLog(
            id=f"log-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            agent_name=agent_name,
            action=action,
            tool_name=tool_name,
            input_data=input_data or {},
            output_data=output_data or {},
            status=status,
            message=message
        )
        self.logs.insert(0, log_entry)  # Prepend newest
        return log_entry

    def get_logs(self, limit: int = 50) -> List[AgentLog]:
        return self.logs[:limit]

    def create_workflow(self, request: str, plan: List[str] = None) -> WorkflowRun:
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        wf = WorkflowRun(
            id=workflow_id,
            request=request,
            status="INITIALIZED",
            plan=plan or [],
            current_step=0,
            results={}
        )
        self.workflows[workflow_id] = wf
        return wf

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowRun]:
        return self.workflows.get(workflow_id)

    def update_workflow(self, workflow_id: str, updates: Dict[str, Any]) -> Optional[WorkflowRun]:
        if workflow_id not in self.workflows:
            return None
        wf = self.workflows[workflow_id]
        wf_dict = wf.model_dump()
        for k, v in updates.items():
            if k in wf_dict:
                wf_dict[k] = v
        wf_dict["updated_at"] = datetime.utcnow()
        updated_wf = WorkflowRun(**wf_dict)
        self.workflows[workflow_id] = updated_wf
        return updated_wf

# Global singleton mock database
mock_db = MockDatabase()
