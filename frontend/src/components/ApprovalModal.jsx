import React, { useState } from 'react';
import { ShieldAlert, Check, X, Mail, AlertTriangle } from 'lucide-react';

export default function ApprovalModal({ isOpen, approvalData, onApprove, onReject, isSubmitting }) {
  const [comments, setComments] = useState('');

  if (!isOpen || !approvalData) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
        
        {/* Header */}
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">
              Supervisor Human-in-the-Loop Gate
            </h3>
            <p className="text-xs text-slate-400">
              High-impact external action paused pending human authorization
            </p>
          </div>
        </div>

        {/* Action summary box */}
        <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 mb-4 text-xs space-y-2.5">
          <div className="flex items-center justify-between text-slate-400">
            <span className="font-semibold text-slate-200">Action:</span>
            <span className="font-mono text-indigo-400">{approvalData.action || 'External Email Outreach'}</span>
          </div>

          {approvalData.recipient && (
            <div className="flex items-center justify-between text-slate-400">
              <span className="font-semibold text-slate-200">Recipient:</span>
              <span className="text-slate-300 font-mono">{approvalData.recipient}</span>
            </div>
          )}

          {approvalData.subject && (
            <div className="text-slate-400">
              <span className="font-semibold text-slate-200 block mb-1">Subject:</span>
              <span className="text-slate-200 bg-slate-900 px-2 py-1 rounded block">{approvalData.subject}</span>
            </div>
          )}

          {approvalData.preview && (
            <div className="text-slate-400">
              <span className="font-semibold text-slate-200 block mb-1">Generated Draft:</span>
              <div className="bg-slate-900/90 p-3 rounded text-slate-300 italic border border-slate-800 leading-relaxed max-h-36 overflow-y-auto">
                {approvalData.preview}
              </div>
            </div>
          )}
        </div>

        {/* Comments input */}
        <div className="mb-5">
          <label className="block text-xs font-medium text-slate-300 mb-1.5">
            Supervisor Notes / Instructions (Optional):
          </label>
          <input
            type="text"
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            placeholder="e.g. Approved with discount pricing adjustment"
            className="w-full bg-slate-950 border border-slate-700/80 rounded-lg px-3 py-2 text-xs text-slate-200 outline-none focus:border-indigo-500"
          />
        </div>

        {/* Modal Buttons */}
        <div className="flex items-center justify-end gap-2.5">
          <button
            type="button"
            onClick={() => onReject(comments)}
            disabled={isSubmitting}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-slate-800 hover:bg-rose-950/40 hover:text-rose-300 border border-slate-700 text-slate-300 text-xs font-medium transition"
          >
            <X className="w-3.5 h-3.5" />
            <span>Reject Action</span>
          </button>

          <button
            type="button"
            onClick={() => onApprove(comments)}
            disabled={isSubmitting}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium shadow-md shadow-emerald-600/20 transition"
          >
            <Check className="w-3.5 h-3.5" />
            <span>Approve & Dispatch</span>
          </button>
        </div>

      </div>
    </div>
  );
}
