import sqlite3
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../bizforce.db"))

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite database tables and seeds 10 fictional leads if table is empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Leads Table (id, name, company, budget, requirement, urgency, score, priority, status, created_at, plus email, title, notes, tags)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        company TEXT NOT NULL,
        budget REAL NOT NULL,
        requirement TEXT NOT NULL,
        urgency TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        priority TEXT DEFAULT 'MEDIUM',
        status TEXT DEFAULT 'NEW',
        created_at TEXT NOT NULL,
        email TEXT,
        title TEXT,
        notes TEXT,
        tags TEXT
    )
    """)

    # 2. Workflows Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflows (
        id TEXT PRIMARY KEY,
        request TEXT NOT NULL,
        status TEXT NOT NULL,
        plan TEXT NOT NULL,
        current_step INTEGER DEFAULT 0,
        results TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 3. Workflow Events / Agent Activity Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_events (
        id TEXT PRIMARY KEY,
        workflow_id TEXT,
        timestamp TEXT NOT NULL,
        agent_name TEXT NOT NULL,
        action TEXT NOT NULL,
        tool_name TEXT,
        input_data TEXT,
        output_data TEXT,
        status TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)

    # 4. Approvals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS approvals (
        id TEXT PRIMARY KEY,
        workflow_id TEXT NOT NULL,
        action_type TEXT NOT NULL,
        target_lead_id TEXT,
        recipient_email TEXT,
        recipient_name TEXT,
        subject TEXT,
        message_body TEXT,
        status TEXT NOT NULL DEFAULT 'PENDING',
        created_at TEXT NOT NULL,
        decision_at TEXT,
        decision_notes TEXT,
        execution_status TEXT DEFAULT 'PENDING',
        execution_result TEXT
    )
    """)

    # 5. Sent Messages (Mock Email tool audit log)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sent_messages (
        id TEXT PRIMARY KEY,
        approval_id TEXT UNIQUE,
        workflow_id TEXT,
        lead_id TEXT,
        recipient TEXT,
        subject TEXT,
        body TEXT,
        sent_at TEXT NOT NULL,
        provider TEXT DEFAULT 'mock_email_tool'
    )
    """)

    conn.commit()

    # Seed 10 realistic fictional leads if none exist
    cursor.execute("SELECT COUNT(*) FROM leads")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_leads = [
            (
                "lead-1", "Sarah Jenkins", "Apex Logistics", 75000.0,
                "Automated warehouse dispatch orchestration and live courier routing",
                "HIGH", 0, "HIGH", "NEW",
                datetime.utcnow().isoformat(),
                "sarah.jenkins@apexlogistics.io", "VP of Operations",
                "Inquired via website demo form regarding fleet dispatch automation.",
                json.dumps(["SupplyChain", "Inbound", "HighPriority"])
            ),
            (
                "lead-2", "David Zhang", "Nexus Health", 40000.0,
                "HIPAA-compliant digital patient intake pipeline and EHR syncing",
                "MEDIUM", 0, "MEDIUM", "NEW",
                datetime.utcnow().isoformat(),
                "dzhang@nexushealth.org", "Director of Digital Health",
                "Downloaded whitepaper on medical intake compliance.",
                json.dumps(["Healthcare", "Intake"])
            ),
            (
                "lead-3", "Elena Rostova", "FinEdge Global", 120000.0,
                "Multi-channel automated client KYC verification and risk scoring",
                "CRITICAL", 0, "HIGH", "NEW",
                datetime.utcnow().isoformat(),
                "elena.r@finedge.com", "Head of Customer Experience",
                "Enterprise client looking to overhaul KYC workflow within 30 days.",
                json.dumps(["FinTech", "Enterprise", "KYC"])
            ),
            (
                "lead-4", "Marcus Vance", "Solaria Energy", 35000.0,
                "Smart ticketing for solar array technician field maintenance",
                "LOW", 0, "LOW", "NEW",
                datetime.utcnow().isoformat(),
                "m.vance@solariaenergy.com", "CTO",
                "Looking for demo on maintenance ticketing.",
                json.dumps(["CleanTech", "FieldOps"])
            ),
            (
                "lead-5", "Amara Okafor", "Meridian Retail", 95000.0,
                "Unified inventory reconciliation and predictive restocking alerts",
                "HIGH", 0, "HIGH", "NEW",
                datetime.utcnow().isoformat(),
                "amara.okafor@meridianretail.com", "Chief Commercial Officer",
                "Multi-store retailer experiencing stockouts across 45 locations.",
                json.dumps(["Retail", "Omnichannel"])
            ),
            (
                "lead-6", "Liam Gallagher", "AeroParts Direct", 60000.0,
                "Automated supplier quote generation and RFQ response workflows",
                "MEDIUM", 0, "MEDIUM", "NEW",
                datetime.utcnow().isoformat(),
                "lgallagher@aeropartsdirect.com", "Procurement Manager",
                "Seeking faster RFQ turnaround times for aerospace parts.",
                json.dumps(["Manufacturing", "Aerospace"])
            ),
            (
                "lead-7", "Priya Patel", "BioGenix Labs", 150000.0,
                "Clinical trial sample logistics tracking and regulatory compliance audits",
                "HIGH", 0, "HIGH", "NEW",
                datetime.utcnow().isoformat(),
                "ppatel@biogenixlabs.org", "VP Clinical Operations",
                "High-budget pharmaceutical research team requiring strict audit trails.",
                json.dumps(["BioTech", "Pharma", "Enterprise"])
            ),
            (
                "lead-8", "Carlos Mendez", "UrbanFleet Rentals", 25000.0,
                "Self-service mobile booking intake and vehicle return inspection logs",
                "LOW", 0, "LOW", "NEW",
                datetime.utcnow().isoformat(),
                "carlos.m@urbanfleetrentals.com", "Fleet Manager",
                "Small car rental agency looking to digitize vehicle checklists.",
                json.dumps(["Mobility", "SMB"])
            ),
            (
                "lead-9", "Chloe Dupont", "HauteCouture Online", 80000.0,
                "Personalized cart abandonment recovery and VIP client concierge",
                "HIGH", 0, "HIGH", "NEW",
                datetime.utcnow().isoformat(),
                "chloe@hautecouture.fr", "Head of E-Commerce",
                "Luxury e-commerce brand seeking AI concierge outreach for high-value orders.",
                json.dumps(["E-Commerce", "Luxury"])
            ),
            (
                "lead-10", "Kenji Takahashi", "NeoRobotics Industrial", 110000.0,
                "Automated telemetry alert triaging for factory robotic arms",
                "CRITICAL", 0, "HIGH", "NEW",
                datetime.utcnow().isoformat(),
                "k.takahashi@neorobotics.jp", "VP of Engineering",
                "Smart factory robotics deployment needing immediate predictive alert triaging.",
                json.dumps(["Robotics", "Industry4.0", "Urgent"])
            )
        ]
        cursor.executemany("""
        INSERT INTO leads (
            id, name, company, budget, requirement, urgency, score, priority, status,
            created_at, email, title, notes, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_leads)
        conn.commit()

    conn.close()

# Lead database operations
def db_get_leads(status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM leads WHERE status = ? ORDER BY score DESC, budget DESC", (status,))
    else:
        cursor.execute("SELECT * FROM leads ORDER BY score DESC, budget DESC")
    rows = cursor.fetchall()
    leads = []
    for r in rows:
        d = dict(r)
        if d.get("tags"):
            try:
                d["tags"] = json.loads(d["tags"])
            except Exception:
                d["tags"] = []
        else:
            d["tags"] = []
        leads.append(d)
    conn.close()
    return leads

def db_get_lead(lead_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if d.get("tags"):
        try:
            d["tags"] = json.loads(d["tags"])
        except Exception:
            d["tags"] = []
    return d

def db_update_lead(lead_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    set_clauses = []
    values = []
    for k, v in updates.items():
        if k == "tags" and isinstance(v, list):
            v = json.dumps(v)
        set_clauses.append(f"{k} = ?")
        values.append(v)
        
    values.append(lead_id)
    query = f"UPDATE leads SET {', '.join(set_clauses)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return db_get_lead(lead_id)

# Workflow operations
def db_create_workflow(request: str, plan: List[str]) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    wf_id = f"wf-{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO workflows (id, request, status, plan, current_step, results, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (wf_id, request, "RUNNING", json.dumps(plan), 0, json.dumps({}), now, now))
    conn.commit()
    conn.close()
    return db_get_workflow(wf_id)

def db_get_workflow(workflow_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workflows WHERE id = ?", (workflow_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["plan"] = json.loads(d["plan"]) if d.get("plan") else []
    d["results"] = json.loads(d["results"]) if d.get("results") else {}
    return d

def db_update_workflow(workflow_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    set_clauses = []
    values = []
    for k, v in updates.items():
        if k in ("plan", "results") and isinstance(v, (dict, list)):
            v = json.dumps(v)
        set_clauses.append(f"{k} = ?")
        values.append(v)
    set_clauses.append("updated_at = ?")
    values.append(datetime.utcnow().isoformat())
    values.append(workflow_id)

    query = f"UPDATE workflows SET {', '.join(set_clauses)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return db_get_workflow(workflow_id)

# Workflow Events / Agent Activity Logs
def db_add_event(workflow_id: Optional[str], agent_name: str, action: str,
                 tool_name: Optional[str] = None,
                 input_data: Optional[Dict[str, Any]] = None,
                 output_data: Optional[Dict[str, Any]] = None,
                 status: str = "SUCCESS", message: str = "") -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    event_id = f"evt-{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO workflow_events (
        id, workflow_id, timestamp, agent_name, action, tool_name,
        input_data, output_data, status, message
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_id, workflow_id, now, agent_name, action, tool_name,
        json.dumps(input_data or {}), json.dumps(output_data or {}), status, message
    ))
    conn.commit()
    conn.close()
    return {
        "id": event_id,
        "workflow_id": workflow_id,
        "timestamp": now,
        "agent_name": agent_name,
        "action": action,
        "tool_name": tool_name,
        "input_data": input_data or {},
        "output_data": output_data or {},
        "status": status,
        "message": message
    }

def db_get_events(workflow_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if workflow_id:
        cursor.execute("SELECT * FROM workflow_events WHERE workflow_id = ? ORDER BY timestamp DESC LIMIT ?", (workflow_id, limit))
    else:
        cursor.execute("SELECT * FROM workflow_events ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    events = []
    for r in rows:
        d = dict(r)
        d["input_data"] = json.loads(d["input_data"]) if d.get("input_data") else {}
        d["output_data"] = json.loads(d["output_data"]) if d.get("output_data") else {}
        events.append(d)
    return events

# Approvals operations
def db_create_approval(workflow_id: str, action_type: str, target_lead_id: str,
                       recipient_email: str, recipient_name: str,
                       subject: str, message_body: str) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    app_id = f"appr-{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO approvals (
        id, workflow_id, action_type, target_lead_id, recipient_email, recipient_name,
        subject, message_body, status, created_at, execution_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, 'PENDING')
    """, (
        app_id, workflow_id, action_type, target_lead_id, recipient_email,
        recipient_name, subject, message_body, now
    ))
    conn.commit()
    conn.close()
    return db_get_approval(app_id)

def db_get_approval(approval_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM approvals WHERE id = ?", (approval_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if d.get("execution_result"):
        try:
            d["execution_result"] = json.loads(d["execution_result"])
        except Exception:
            pass
    return d

def db_get_approvals(status: Optional[str] = None, workflow_id: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM approvals"
    conditions = []
    params = []
    if status:
        conditions.append("status = ?")
        params.append(status)
    if workflow_id:
        conditions.append("workflow_id = ?")
        params.append(workflow_id)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    approvals = []
    for r in rows:
        d = dict(r)
        if d.get("execution_result"):
            try:
                d["execution_result"] = json.loads(d["execution_result"])
            except Exception:
                pass
        approvals.append(d)
    return approvals

def db_record_sent_message(approval_id: str, workflow_id: str, lead_id: str,
                           recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """Records approved message in SQLite sent_messages table. Idempotent via UNIQUE constraint."""
    conn = get_connection()
    cursor = conn.cursor()
    msg_id = f"msg-{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT OR IGNORE INTO sent_messages (
        id, approval_id, workflow_id, lead_id, recipient, subject, body, sent_at, provider
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'mock_email_tool')
    """, (msg_id, approval_id, workflow_id, lead_id, recipient, subject, body, now))
    conn.commit()
    conn.close()
    return {
        "id": msg_id,
        "approval_id": approval_id,
        "recipient": recipient,
        "subject": subject,
        "sent_at": now,
        "status": "SENT_VIA_MOCK_TOOL"
    }

# Initialize database on module load
init_db()
