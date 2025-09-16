import React from "react";
import type { EvalItem, ModelKey } from "../types";

export default function DetailModal({ open, onClose, model, evals, team }:{ open:boolean; onClose:()=>void; model:ModelKey|null; evals:EvalItem[]; team:any }){
  if (!open || !model) return null;
  const received = evals.filter(e => e.target===model);
  return (
    <div className="fixed inset-0 z-50">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div className="relative mx-auto my-6 w-[min(95vw,900px)] max-h-[85vh] card p-4 overflow-y-auto">
        <div className="flex items-center justify-between mb-2">
          <div className="font-semibold">상세 분석 — {model.toUpperCase()}</div>
          <button className="btn" onClick={onClose}>닫기</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="card p-3"><div className="font-semibold">Leader</div><div className="text-sm whitespace-pre-wrap">{team?.leader}</div></div>
          <div className="card p-3"><div className="font-semibold">Blue</div><div className="text-sm whitespace-pre-wrap">{team?.blue}</div></div>
          <div className="card p-3"><div className="font-semibold">Research</div><div className="text-sm whitespace-pre-wrap">{team?.research}</div></div>
          <div className="card p-3"><div className="font-semibold">Red</div><div className="text-sm whitespace-pre-wrap">{team?.red}</div></div>
        </div>
        <div className="card p-3 mt-3 bg-[var(--surface-high)]"><div className="font-semibold">리더 요약</div><div className="text-sm whitespace-pre-wrap">{team?.summary}</div></div>
        <div className="mt-3"><div className="font-semibold mb-1">받은 평가(사유 포함)</div>
          <div className="space-y-2">{received.map((e,i)=>(
            <div key={i} className="card p-3">
              <div className="text-xs text-[var(--text-muted)] mb-1">Evaluator: {e.evaluator.toUpperCase()} / 총점 {e.total}</div>
              <ul className="text-sm space-y-1">{e.scores.map((s,j)=>(<li key={j}><b>{s.criterion}</b> — {s.score}점 · <span className="text-[var(--text-muted)]">{s.reason}</span></li>))}</ul>
            </div>
          ))}</div>
        </div>
      </div>
    </div>
  );
}
