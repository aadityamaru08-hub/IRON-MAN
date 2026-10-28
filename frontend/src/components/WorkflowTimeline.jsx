import React from 'react';
import { Network, UserCheck, Database, Mail, ShieldAlert, CheckCircle2, Clock } from 'lucide-react';

const AGENT_STAGES = [
  {
    key: 'orchestrator',
    title: 'Orchestrator Agent',
    desc: 'Interprets request & designs task plan',
    icon: Network,
    badge: 'LangGraph Planner'
  },
  {
    key: 'qualification',
    title: 'Lead Qualification Agent',
    desc: 'Analyzes intent, budget, fit & scores leads',
    icon: UserCheck,
    badge: 'AI Analyzer'
  },
  {
    key: 'crm',
    title: 'CRM Agent',
    desc: 'Updates contact stages & CRM database',
    icon: Database,
    badge: 'Tool Executor'
  },
  {
    key: 'outreach',
    title: 'Outreach Agent',
    desc: 'Generates tailored follow-up messages',
    icon: Mail,
    badge: 'Copy Synthesizer'
  },
  {
    key: 'supervisor',
    title: 'Supervisor Agent',
    desc: 'Audits quality & halts for human approval',
    icon: ShieldAlert,
    badge: 'Human-in-the-Loop'
  }
];

export default function WorkflowTimeline({ currentWorkflow }) {
  const currentStep = currentWorkflow?.current_step || 0;
  const isCompleted = currentWorkflow?.status === 'COMPLETED';

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div>
          <h2 className="text-sm font-semibold tracking-wide uppercase text-slate-300">
            Multi-Agent Orchestration Pipeline
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time step execution graph managed via LangGraph
          </p>
        </div>
        {currentWorkflow && (
          <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            Workflow: {currentWorkflow.id}
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
        {AGENT_STAGES.map((stage, idx) => {
          const stepNumber = idx + 1;
          const isDone = isCompleted || currentStep > stepNumber;
          const isActive = currentStep === stepNumber;
          const isPending = currentStep < stepNumber;

          const IconComponent = stage.icon;

          return (
            <div
              key={stage.key}
              className={`relative p-3.5 rounded-xl border transition-all ${
                isActive
                  ? 'bg-indigo-950/40 border-indigo-500 shadow-md shadow-indigo-500/10 ring-1 ring-indigo-500/30'
                  : isDone
                  ? 'bg-slate-900/40 border-emerald-500/30 text-slate-300'
                  : 'bg-slate-950/40 border-slate-800/80 text-slate-500'
              }`}
            >
              {/* Header with icon and status */}
              <div className="flex items-center justify-between mb-2">
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center ${
                    isActive
                      ? 'bg-indigo-600 text-white animate-pulse'
                      : isDone
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  <IconComponent className="w-4 h-4" />
                </div>
                <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-slate-800/60 border border-slate-700/50">
                  Step {stepNumber}
                </span>
              </div>

              {/* Title & Desc */}
              <h3 className={`text-xs font-semibold mb-1 ${isActive ? 'text-indigo-200' : isDone ? 'text-slate-200' : 'text-slate-400'}`}>
                {stage.title}
              </h3>
              <p className="text-[11px] text-slate-400 leading-relaxed mb-2.5 line-clamp-2">
                {stage.desc}
              </p>

              {/* State pill */}
              <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px]">
                <span className="text-slate-500 font-medium">{stage.badge}</span>
                {isDone ? (
                  <span className="text-emerald-400 font-medium flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" /> Done
                  </span>
                ) : isActive ? (
                  <span className="text-indigo-400 font-medium flex items-center gap-1">
                    <Clock className="w-3 h-3 animate-spin" /> Active
                  </span>
                ) : (
                  <span className="text-slate-600">Pending</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Plan list display if active */}
      {currentWorkflow?.plan?.length > 0 && (
        <div className="mt-4 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Active Task Plan Synthesized by Orchestrator:
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-300">
            {currentWorkflow.plan.map((step, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                <span className="truncate">{step}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
