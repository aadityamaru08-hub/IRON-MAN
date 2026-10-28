from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Lead(BaseModel):
    id: str
    name: str
    company: str
    email: str
    title: str = "Lead"
    status: str = "NEW"  # NEW, QUALIFIED, UNQUALIFIED, CONTACTED, CLOSED
    score: int = 0       # 0 - 100
    notes: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AgentLog(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_name: str
    action: str
    tool_name: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    status: str = "SUCCESS"  # SUCCESS, PENDING, REQUIRE_APPROVAL, REJECTED, ERROR
    message: str

class WorkflowRun(BaseModel):
    id: str
    request: str
    status: str = "INITIALIZED"  # INITIALIZED, RUNNING, PAUSED_APPROVAL, COMPLETED, FAILED
    plan: List[str] = Field(default_factory=list)
    current_step: int = 0
    pending_approval: Optional[Dict[str, Any]] = None
    results: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
