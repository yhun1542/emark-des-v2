import React from "react";
import type { TeamState } from "../types";
function Bar({ value }:{value:number}){
  return <div className="h-2 bg-[var(--surface-high)] rounded"><div className="h-2 rounded" style={{ width:`${value}%`, background:"linear-gradient(90deg,#9d4edd,#42a9ff)" }} /></div>;
}
export default function TeamGrid({ teams }:{ teams:TeamState[] }){
  const box = (title:string, body?:string)=> (
    <div className="card p-3">
      <div className="text-xs text-[var(--text-muted)]">{title}</div>
      <div className={`text-sm whitespace-pre-wrap mt-1 ${body?"":"skeleton h-12 rounded"}`}>{body||""}</div>
    </div>
  );
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
      {teams.map(t=> (
        <div key={t.model} className="card p-3">
          <div className="flex items-center justify-between mb-2"><div className="badge">{t.model.toUpperCase()}</div><div className="text-xs text-[var(--text-muted)]">{t.status}</div></div>
          <Bar value={t.progress} />
          <div className="mt-2 grid gap-2">
            {box("Leader", t.leader?.content)}
            {box("Blue", t.blue?.content)}
            {box("Research", t.research?.content)}
            {box("Red", t.red?.content)}
          </div>
          <div className="mt-2 card p-2 bg-[var(--surface-high)]">
            <div className="text-sm font-semibold">리더 요약</div>
            <div className={`text-sm whitespace-pre-wrap mt-1 ${t.summary?"":"skeleton h-10 rounded"}`}>{t.summary||""}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
