import React from 'react';
import { Activity, Database, Sparkles, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';

export default function Header({ backendHealth, isChecking, onRefresh }) {
  const isHealthy = backendHealth && backendHealth.status === 'healthy';

  return (
    <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-30 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        
        {/* Brand identity */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/20 ring-1 ring-white/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">BizForce AI</h1>
              <span className="px-2 py-0.5 text-xs font-semibold uppercase tracking-wider rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                MVP v0.1
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Autonomous Multi-Agent Business Automation Engine
            </p>
          </div>
        </div>

        {/* System telemetry & connection badges */}
        <div className="flex flex-wrap items-center gap-2.5 text-xs">
          {/* Backend Status */}
          <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border font-medium transition-all ${
            isHealthy 
              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' 
              : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
          }`}>
            {isHealthy ? (
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
            ) : (
              <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
            )}
            <span>Backend: {isHealthy ? 'FastAPI Online' : 'Connecting...'}</span>
          </div>

          {/* Database mode */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-slate-300">
            <Database className="w-3.5 h-3.5 text-sky-400" />
            <span>DB: SQLite</span>
          </div>

          {/* AI Engine */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-slate-300">
            <Activity className="w-3.5 h-3.5 text-indigo-400" />
            <span>AI: {backendHealth?.has_anthropic_key ? 'Claude 3.5 Sonnet' : 'Deterministic Fallback'}</span>
          </div>

          {/* Refresh connection button */}
          <button
            onClick={onRefresh}
            disabled={isChecking}
            title="Check backend health"
            className="p-1.5 rounded-lg bg-slate-800 border border-slate-700/60 text-slate-400 hover:text-white hover:bg-slate-700 transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isChecking ? 'animate-spin text-indigo-400' : ''}`} />
          </button>
        </div>

      </div>
    </header>
  );
}
