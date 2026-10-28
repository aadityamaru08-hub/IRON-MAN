import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import RequestInput from './components/RequestInput';
import WorkflowTimeline from './components/WorkflowTimeline';
import LeadViewer from './components/LeadViewer';
import AgentActivityLog from './components/AgentActivityLog';
import ApprovalModal from './components/ApprovalModal';
import {
  checkBackendHealth, fetchLeads, fetchAgentLogs,
  runWorkflow, fetchApprovals, approveApproval, rejectApproval
} from './services/api';
import { ShieldAlert, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function App() {
  const [backendHealth, setBackendHealth] = useState(null);
  const [isCheckingHealth, setIsCheckingHealth] = useState(false);
  const [leads, setLeads] = useState([]);
  const [logs, setLogs] = useState([]);
  const [pendingApprovals, setPendingApprovals] = useState([]);
  const [currentWorkflow, setCurrentWorkflow] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [approvalModal, setApprovalModal] = useState({ isOpen: false, data: null });
  const [isSubmittingApproval, setIsSubmittingApproval] = useState(false);

  // Initial connection check & load data from SQLite backend
  const loadSystemState = async () => {
    setIsCheckingHealth(true);
    try {
      const health = await checkBackendHealth();
      setBackendHealth(health);

      const [leadsData, logsData, approvalsData] = await Promise.all([
        fetchLeads(),
        fetchAgentLogs(35),
        fetchApprovals('PENDING')
      ]);
      setLeads(leadsData);
      setLogs(logsData);
      setPendingApprovals(approvalsData);
    } catch (err) {
      console.warn('Backend connection error:', err);
      setBackendHealth({ status: 'error', message: err.message });
    } finally {
      setIsCheckingHealth(false);
    }
  };

  useEffect(() => {
    loadSystemState();
    // Poll for background events every 6 seconds
    const interval = setInterval(() => {
      fetchLeads().then(setLeads).catch(() => {});
      fetchAgentLogs(35).then(setLogs).catch(() => {});
      fetchApprovals('PENDING').then(setPendingApprovals).catch(() => {});
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  // Launch multi-agent workflow
  const handleLaunchWorkflow = async (requestText) => {
    setIsExecuting(true);
    try {
      const wf = await runWorkflow(requestText);
      setCurrentWorkflow(wf);

      // Re-fetch all data to show real SQLite state updates
      const [updatedLeads, updatedLogs, updatedApprovals] = await Promise.all([
        fetchLeads(),
        fetchAgentLogs(35),
        fetchApprovals('PENDING', wf.id)
      ]);
      setLeads(updatedLeads);
      setLogs(updatedLogs);
      setPendingApprovals(updatedApprovals);

      // If workflow paused for approval, open modal automatically for the first pending item
      if (wf.status === 'PAUSED_APPROVAL' && updatedApprovals.length > 0) {
        openApproval(updatedApprovals[0]);
      }
    } catch (err) {
      alert(`Workflow execution error: ${err.message}`);
    } finally {
      setIsExecuting(false);
    }
  };

  const openApproval = (approval) => {
    setApprovalModal({
      isOpen: true,
      data: {
        id: approval.id,
        action: approval.action_type === 'SEND_EMAIL' ? 'Dispatch Personalized Outreach Email' : approval.action_type,
        recipient: `${approval.recipient_name} <${approval.recipient_email}>`,
        subject: approval.subject,
        preview: approval.message_body
      }
    });
  };

  // Human approval handlers
  const handleApprove = async (comments) => {
    if (!approvalModal.data?.id) return;
    setIsSubmittingApproval(true);
    try {
      await approveApproval(approvalModal.data.id, comments);
      setApprovalModal({ isOpen: false, data: null });
      await loadSystemState();
    } catch (err) {
      alert(`Approval error: ${err.message}`);
    } finally {
      setIsSubmittingApproval(false);
    }
  };

  const handleReject = async (comments) => {
    if (!approvalModal.data?.id) return;
    setIsSubmittingApproval(true);
    try {
      await rejectApproval(approvalModal.data.id, comments);
      setApprovalModal({ isOpen: false, data: null });
      await loadSystemState();
    } catch (err) {
      alert(`Rejection error: ${err.message}`);
    } finally {
      setIsSubmittingApproval(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navbar */}
      <Header
        backendHealth={backendHealth}
        isChecking={isCheckingHealth}
        onRefresh={loadSystemState}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        
        {/* Banner if backend is not yet started */}
        {backendHealth?.status === 'error' && (
          <div className="bg-rose-950/40 border border-rose-500/40 rounded-xl p-4 text-xs text-rose-300 flex items-center justify-between">
            <div>
              <span className="font-semibold block text-rose-200 mb-0.5">FastAPI Backend Disconnected</span>
              Make sure to run <code className="bg-rose-900/40 px-1.5 py-0.5 rounded font-mono">python3 backend/run.py</code> in a terminal.
            </div>
            <button
              onClick={loadSystemState}
              className="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-medium transition"
            >
              Retry Connection
            </button>
          </div>
        )}

        {/* Pending Human Approval Banner */}
        {pendingApprovals.length > 0 && (
          <div className="bg-amber-950/40 border border-amber-500/40 rounded-2xl p-4 shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 animate-in fade-in">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-amber-200">
                  {pendingApprovals.length} High-Impact Action{pendingApprovals.length > 1 ? 's' : ''} Awaiting Human Authorization
                </h3>
                <p className="text-xs text-amber-300/80">
                  Supervisor agent halted workflow before external email dispatch to {pendingApprovals[0].recipient_name}.
                </p>
              </div>
            </div>
            <button
              onClick={() => openApproval(pendingApprovals[0])}
              className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs transition flex items-center gap-1.5 shadow-md shadow-amber-500/20 shrink-0"
            >
              <span>Review Action</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* User Request Input */}
        <RequestInput
          onSubmit={handleLaunchWorkflow}
          isLoading={isExecuting}
          disabled={backendHealth?.status === 'error'}
        />

        {/* Multi-Agent Orchestration Pipeline */}
        <WorkflowTimeline currentWorkflow={currentWorkflow} />

        {/* Two-column layout: CRM Leads (Left) and Agent Logs / Tools (Right) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
          <LeadViewer
            leads={leads}
            isLoading={isCheckingHealth}
            onRefresh={async () => setLeads(await fetchLeads())}
          />

          <AgentActivityLog
            logs={logs}
            onRefresh={async () => setLogs(await fetchAgentLogs(35))}
          />
        </div>
      </main>

      {/* Human-in-the-Loop Approval Modal */}
      <ApprovalModal
        isOpen={approvalModal.isOpen}
        approvalData={approvalModal.data}
        onApprove={handleApprove}
        onReject={handleReject}
        isSubmitting={isSubmittingApproval}
      />

      {/* Simple Hackathon Footer */}
      <footer className="border-t border-slate-900 py-4 text-center text-xs text-slate-500">
        BizForce AI &bull; Built with React + FastAPI + SQLite &bull; Multi-Agent Workflow Engine
      </footer>
    </div>
  );
}
