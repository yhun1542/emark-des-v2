import React from "react";
import type { EvalItem, ModelKey } from "../types";

export default function Matrix({ evals }:{ evals: EvalItem[] }){
  const models: ModelKey[] = ["gemini","grok","chatgpt","claude"];
  const score = (ev:ModelKey, tar:ModelKey) => evals.find(e=>e.evaluator===ev && e.target===tar)?.total ?? null;
  const cls = (v:number|null) => v===null? "bg-[var(--surface-high)] text-[var(--text-muted)]" : v>=90? "text-green-400 font-semibold" : v<=83? "text-red-400" : "text-yellow-300";
  return (
    <div className="overflow-x-auto">
      <table className="min-w-[560px] w-full text-sm border border-[var(--surface-border)]">
        <thead><tr><th className="p-2 text-left border border-[var(--surface-border)]">평가자\\피평가자</th>{models.map(m=><th key={m} className="p-2 border border-[var(--surface-border)]">{m.toUpperCase()}</th>)}</tr></thead>
        <tbody>
          {models.map(ev=>(
            <tr key={ev}>
              <td className="p-2 border border-[var(--surface-border)]">{ev.toUpperCase()}</td>
              {models.map(t => <td key={t} className={`p-2 text-center border border-[var(--surface-border)] ${cls(ev===t?null:score(ev,t))}`}>{ev===t?"—":score(ev,t)}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
