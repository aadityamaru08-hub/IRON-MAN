# BizForce AI ⚡
> Autonomous Multi-Agent Business Automation Engine for Lead Qualification, CRM Updates, and Personalized Outreach.

Built with **FastAPI**, **SQLite**, **Pydantic**, **React (Vite + Tailwind CSS)**, and **Claude API (with deterministic fallback)**.

---

## 🏗️ Architecture & Database Design

BizForce AI uses a persistent **SQLite database** (`bizforce.db` at project root) containing:

1. **`leads`**: `id`, `name`, `company`, `budget`, `requirement`, `urgency`, `score`, `priority`, `status`, `created_at`, `email`, `title`, `notes`, `tags`
2. **`workflows`**: `id`, `request`, `status`, `plan`, `current_step`, `results`, `created_at`, `updated_at`
3. **`workflow_events`**: Real-time event & tool execution audit log with agent names, inputs, and outputs.
4. **`approvals`**: Human-in-the-loop action gate with idempotency checks and approval state.
5. **`sent_messages`**: Mock email audit table recording all approved messages. Never transmits real emails.

---

## ⚡ Quickstart Commands

### 1. Install Backend Dependencies
From the project folder (`~/Desktop/anti`):
```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment (Optional)
If you want to use live Claude API:
```bash
cp backend/.env.example backend/.env
# Add your key: ANTHROPIC_API_KEY=sk-ant-...
```
> **Note**: If `ANTHROPIC_API_KEY` is not provided, the application runs transparently using a deterministic rule-based qualification & outreach engine. It never pretends an LLM was used when it wasn't.

### 3. Start the FastAPI Backend
```bash
python3 backend/run.py
```
- Server: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 4. Start or View the React Frontend
The React frontend runs at:
```bash
cd frontend
npm run dev
```
Accessible at: **`http://localhost:5174`** (or `http://localhost:5173`)

---

## 🧪 Testing the Complete Workflow

### Automated CLI Test
Run the test script to test all 7 endpoints, qualification, tool execution, and approval idempotency:
```bash
python3 -c "
import httpx
client = httpx.Client(base_url='http://127.0.0.1:8000')

# 1. Health
print('Health:', client.get('/health').json())

# 2. Leads (10 seeded records)
leads = client.get('/leads').json()
print(f'Total Leads: {len(leads)}')

# 3. Launch Workflow
wf = client.post('/workflows/run', json={'request': 'Qualify enterprise inbound leads and draft outreach'}).json()
print('Workflow Status:', wf['status'])

# 4. View Pending Approvals
approvals = client.get('/approvals?status=PENDING').json()
print(f'Pending Approvals: {len(approvals)}')

# 5. Approve First Action (Idempotent)
if approvals:
    appr_id = approvals[0]['id']
    res = client.post(f'/approvals/{appr_id}/approve', json={'comments': 'Approved by sales manager'}).json()
    print('Approval Response:', res['message'])
"
```

### UI Workflow Steps
1. Open the dashboard at `http://localhost:5174`.
2. Inspect the **10 Seeded Leads** in the SQLite CRM table.
3. Click one of the **Demo Prompts** or type a request and click **Launch Workflow**.
4. Watch the **Workflow Pipeline** and **Agent Activity Log** execute in real time.
5. The **Supervisor Agent** halts the pipeline before dispatching external emails and displays a **Pending Human Authorization** banner.
6. Click **Review Action**, inspect the personalized email draft, and click **Approve & Dispatch**.
7. The lead status in SQLite automatically updates to `CONTACTED`, and the email dispatch is logged in the `sent_messages` table without sending real emails.

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System telemetry, SQLite status, and AI engine status |
| `GET` | `/leads` | List all 10 CRM leads from SQLite (optional `?status=...` filter) |
| `GET` | `/leads/{id}` | Retrieve single lead by ID |
| `POST` | `/workflows/run` | Launch 5-stage multi-agent orchestration |
| `GET` | `/workflows/{id}` | Inspect workflow state |
| `GET` | `/workflows/logs` | Real-time tool execution & agent log stream |
| `GET` | `/approvals` | List pending / resolved approval requests |
| `POST` | `/approvals/{id}/approve` | Human authorization to execute action (idempotent) |
| `POST` | `/approvals/{id}/reject` | Reject action (idempotent) |
