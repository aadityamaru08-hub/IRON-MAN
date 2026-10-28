/**
 * API Client for BizForce AI FastAPI Backend
 */

const API_BASE = '/api';

export async function checkBackendHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) {
    throw new Error(`Health check failed with status: ${res.status}`);
  }
  return res.json();
}

export async function fetchLeads(status = null) {
  const url = status ? `${API_BASE}/leads?status=${encodeURIComponent(status)}` : `${API_BASE}/leads`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch leads: ${res.status}`);
  }
  return res.json();
}

export async function fetchAgentLogs(limit = 50, workflowId = null) {
  const url = workflowId 
    ? `${API_BASE}/workflows/logs?limit=${limit}&workflow_id=${encodeURIComponent(workflowId)}`
    : `${API_BASE}/workflows/logs?limit=${limit}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch agent logs: ${res.status}`);
  }
  return res.json();
}

export async function runWorkflow(requestText) {
  const res = await fetch(`${API_BASE}/workflows/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ request: requestText })
  });
  if (!res.ok) {
    throw new Error(`Failed to start workflow: ${res.status}`);
  }
  return res.json();
}

export async function getWorkflow(workflowId) {
  const res = await fetch(`${API_BASE}/workflows/${workflowId}`);
  if (!res.ok) {
    throw new Error(`Failed to get workflow ${workflowId}: ${res.status}`);
  }
  return res.json();
}

export async function fetchApprovals(status = null, workflowId = null) {
  const params = new URLSearchParams();
  if (status) params.append('status', status);
  if (workflowId) params.append('workflow_id', workflowId);
  const q = params.toString() ? `?${params.toString()}` : '';
  const res = await fetch(`${API_BASE}/approvals${q}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch approvals: ${res.status}`);
  }
  return res.json();
}

export async function approveApproval(approvalId, comments = '') {
  const res = await fetch(`${API_BASE}/approvals/${approvalId}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ comments })
  });
  if (!res.ok) {
    throw new Error(`Failed to approve action: ${res.status}`);
  }
  return res.json();
}

export async function rejectApproval(approvalId, comments = '') {
  const res = await fetch(`${API_BASE}/approvals/${approvalId}/reject`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ comments })
  });
  if (!res.ok) {
    throw new Error(`Failed to reject action: ${res.status}`);
  }
  return res.json();
}

// Backward compatibility helper
export async function approveWorkflow(workflowId, approved, comments = '') {
  const approvals = await fetchApprovals('PENDING', workflowId);
  if (approvals.length === 0) {
    return getWorkflow(workflowId);
  }
  const target = approvals[0];
  if (approved) {
    await approveApproval(target.id, comments);
  } else {
    await rejectApproval(target.id, comments);
  }
  return getWorkflow(workflowId);
}
