import React, { useState } from 'react';
import { Send, Zap, CornerDownLeft, Sparkles } from 'lucide-react';

const PRESET_REQUESTS = [
  "Qualify inbound leads, update CRM records, and prepare personalized outreach for review.",
  "Identify high-intent enterprise leads, tag them as urgent, and draft executive follow-ups.",
  "Audit all logistics and tech leads, calculate fit scores, and queue demo emails for approval."
];

export default function RequestInput({ onSubmit, isLoading, disabled }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading || disabled) return;
    onSubmit(input.trim());
  };

  const handleSelectPreset = (preset) => {
    setInput(preset);
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden backdrop-blur-sm">
      {/* Glow decorative element */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-48 h-48 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center gap-2 mb-3">
        <Zap className="w-4 h-4 text-amber-400" />
        <h2 className="text-sm font-semibold tracking-wide uppercase text-slate-300">
          Enter Natural-Language Business Request
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={disabled || isLoading}
            placeholder="e.g. Qualify newly received inbound leads, calculate engagement scores, update CRM tags, and draft personalized follow-ups for supervisor sign-off..."
            rows={3}
            className="w-full bg-slate-950/80 border border-slate-700/80 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 outline-none resize-none transition"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading || disabled}
            className="absolute bottom-3 right-3 inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white text-xs font-medium shadow-md shadow-indigo-600/20 transition disabled:shadow-none"
          >
            {isLoading ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Orchestrating...</span>
              </>
            ) : (
              <>
                <span>Launch Workflow</span>
                <Send className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>

        {/* Quick Demo Presets */}
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs text-slate-400">
          <span className="flex items-center gap-1 text-slate-400 font-medium">
            <Sparkles className="w-3 h-3 text-indigo-400" /> Demo Prompts:
          </span>
          {PRESET_REQUESTS.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectPreset(preset)}
              className="text-left px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/50 hover:border-indigo-500/40 text-slate-300 hover:text-white transition truncate max-w-xs"
            >
              {preset}
            </button>
          ))}
        </div>
      </form>
    </div>
  );
}
