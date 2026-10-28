import React from 'react';
import { Users, Mail, Building, DollarSign, Clock, ShieldCheck } from 'lucide-react';

export default function LeadViewer({ leads, isLoading, onRefresh }) {
  const getStatusBadge = (status) => {
    switch (status) {
      case 'QUALIFIED':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'CONTACTED':
        return 'bg-sky-500/10 text-sky-400 border-sky-500/30';
      case 'UNQUALIFIED':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      default:
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    }
  };

  const getUrgencyBadge = (urgency) => {
    switch (urgency) {
      case 'CRITICAL':
        return 'bg-rose-500/20 text-rose-400 border-rose-500/40';
      case 'HIGH':
        return 'bg-amber-500/20 text-amber-400 border-amber-500/40';
      case 'MEDIUM':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/40';
      default:
        return 'bg-slate-700/40 text-slate-400 border-slate-600/40';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-emerald-400 bg-emerald-500';
    if (score >= 45) return 'text-amber-400 bg-amber-500';
    return 'text-slate-400 bg-slate-500';
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Users className="w-4 h-4 text-sky-400" />
          <h2 className="text-sm font-semibold tracking-wide uppercase text-slate-300">
            SQLite CRM Leads & Qualification
          </h2>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
            {leads.length} Records
          </span>
        </div>
        <button
          onClick={onRefresh}
          className="text-xs text-slate-400 hover:text-white transition"
        >
          Refresh CRM
        </button>
      </div>

      <div className="overflow-x-auto max-h-[460px] overflow-y-auto">
        <table className="w-full text-left text-xs">
          <thead className="sticky top-0 bg-slate-900 z-10">
            <tr className="text-slate-400 border-b border-slate-800/80 pb-2">
              <th className="py-2.5 font-medium">Prospect</th>
              <th className="py-2.5 font-medium">Company</th>
              <th className="py-2.5 font-medium">Budget & Urgency</th>
              <th className="py-2.5 font-medium">Status & Priority</th>
              <th className="py-2.5 font-medium">Score</th>
              <th className="py-2.5 font-medium">Requirement & Notes</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {leads.map((lead) => {
              const scoreColor = getScoreColor(lead.score);
              return (
                <tr key={lead.id} className="hover:bg-slate-800/30 transition">
                  {/* Prospect */}
                  <td className="py-3">
                    <div className="font-medium text-slate-200">{lead.name}</div>
                    <div className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                      <Mail className="w-3 h-3 text-slate-500" /> {lead.email || `${lead.name.toLowerCase().replace(' ', '.')}@${lead.company.toLowerCase().replace(' ', '')}.com`}
                    </div>
                  </td>

                  {/* Company */}
                  <td className="py-3">
                    <div className="text-slate-200 font-medium">{lead.company}</div>
                    <div className="text-[11px] text-slate-400">{lead.title || 'Decision Maker'}</div>
                  </td>

                  {/* Budget & Urgency */}
                  <td className="py-3">
                    <div className="text-slate-200 font-mono font-medium">
                      ${Number(lead.budget || 0).toLocaleString()}
                    </div>
                    <span className={`inline-block mt-0.5 px-1.5 py-0.2 rounded text-[10px] font-medium border ${getUrgencyBadge(lead.urgency)}`}>
                      {lead.urgency || 'MEDIUM'}
                    </span>
                  </td>

                  {/* Status & Priority */}
                  <td className="py-3">
                    <div className="flex flex-col gap-1 items-start">
                      <span className={`px-2 py-0.5 rounded-md border text-[11px] font-medium ${getStatusBadge(lead.status)}`}>
                        {lead.status}
                      </span>
                      {lead.priority && (
                        <span className="text-[10px] text-slate-400 uppercase font-mono">
                          Priority: {lead.priority}
                        </span>
                      )}
                    </div>
                  </td>

                  {/* AI Score */}
                  <td className="py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-10 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                        <div
                          className={`h-full rounded-full ${scoreColor.split(' ')[1]}`}
                          style={{ width: `${lead.score}%` }}
                        />
                      </div>
                      <span className="font-mono font-bold text-slate-200">
                        {lead.score}/100
                      </span>
                    </div>
                  </td>

                  {/* Requirement & Notes */}
                  <td className="py-3 max-w-xs">
                    {lead.requirement && (
                      <p className="text-[11px] text-slate-300 line-clamp-1 font-medium mb-0.5">
                        {lead.requirement}
                      </p>
                    )}
                    {lead.notes && (
                      <p className="text-[10px] text-slate-400 line-clamp-1 italic">
                        "{lead.notes}"
                      </p>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
