import React, { useState } from 'react';
import { Terminal, ChevronDown, ChevronRight, Wrench, ShieldCheck, CheckCircle2, AlertCircle } from 'lucide-react';

export default function AgentActivityLog({ logs, onRefresh }) {
  const [expandedId, setExpandedId] = useState(null);

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'SUCCESS':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'REQUIRE_APPROVAL':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'REJECTED':
      case 'ERROR':
        return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
      default:
        return 'text-sky-400 bg-sky-500/10 border-sky-500/20';
    }
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <h2 className="text-sm font-semibold tracking-wide uppercase text-slate-300">
            Agent Activity & Tool Execution Stream
          </h2>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
            {logs.length} Events
          </span>
        </div>
        <button
          onClick={onRefresh}
          className="text-xs text-slate-400 hover:text-white transition"
        >
          Refresh Logs
        </button>
      </div>

      <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-1">
        {logs.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-500">
            No agent activity recorded yet. Launch a workflow to see multi-agent orchestration logs.
          </div>
        ) : (
          logs.map((log) => {
            const isExpanded = expandedId === log.id;
            const hasPayload = log.input_data || log.output_data;
            const timeStr = new Date(log.timestamp).toLocaleTimeString();

            return (
              <div
                key={log.id}
                className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700/80 transition text-xs"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-start gap-2.5 flex-1 min-w-0">
                    <div className="mt-0.5">
                      {log.status === 'SUCCESS' ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      ) : log.status === 'REQUIRE_APPROVAL' ? (
                        <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
                      ) : (
                        <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2 mb-1">
                        <span className="font-semibold text-indigo-300">
                          {log.agent_name}
                        </span>
                        {log.tool_name && (
                          <span className="flex items-center gap-1 font-mono text-[10px] px-1.5 py-0.5 rounded bg-slate-800/80 text-cyan-300 border border-slate-700">
                            <Wrench className="w-2.5 h-2.5" /> {log.tool_name}
                          </span>
                        )}
                        <span className={`text-[10px] px-1.5 py-0.5 rounded border ${getStatusBadge(log.status)}`}>
                          {log.status}
                        </span>
                      </div>
                      <p className="text-slate-300 leading-snug">
                        {log.message}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className="font-mono text-[10px] text-slate-500">
                      {timeStr}
                    </span>
                    {hasPayload && (
                      <button
                        onClick={() => toggleExpand(log.id)}
                        className="text-slate-400 hover:text-white p-1"
                        title="View payload"
                      >
                        {isExpanded ? (
                          <ChevronDown className="w-3.5 h-3.5" />
                        ) : (
                          <ChevronRight className="w-3.5 h-3.5" />
                        )}
                      </button>
                    )}
                  </div>
                </div>

                {/* Expandable tool payload */}
                {isExpanded && (
                  <div className="mt-2.5 pt-2.5 border-t border-slate-800/60 grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] font-mono">
                    {log.input_data && Object.keys(log.input_data).length > 0 && (
                      <div className="bg-slate-900/90 rounded p-2 border border-slate-800">
                        <span className="text-slate-400 text-[10px] block mb-1 uppercase tracking-wider">Tool Input:</span>
                        <pre className="text-slate-300 overflow-x-auto whitespace-pre-wrap">
                          {JSON.stringify(log.input_data, null, 2)}
                        </pre>
                      </div>
                    )}
                    {log.output_data && Object.keys(log.output_data).length > 0 && (
                      <div className="bg-slate-900/90 rounded p-2 border border-slate-800">
                        <span className="text-slate-400 text-[10px] block mb-1 uppercase tracking-wider">Tool Output:</span>
                        <pre className="text-emerald-300 overflow-x-auto whitespace-pre-wrap">
                          {JSON.stringify(log.output_data, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
