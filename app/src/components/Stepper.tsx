import React from "react";
export default function Stepper({ stage }:{ stage:1|2|3 }){
  const items = [{id:1,label:"병렬 구조화 토론"},{id:2,label:"상호 교차 평가"},{id:3,label:"최종 평점 산출"}];
  return (
    <div className="relative flex justify-between mb-3">
      <div className="absolute left-[6%] right-[6%] top-4 h-1 bg-[var(--surface-border)]" />
      {items.map(s=> (
        <div key={s.id} className={`relative z-10 flex flex-col items-center ${s.id<=stage?"opacity-100":"opacity-60"}`}>
          <div className={`w-10 h-10 rounded-full flex items-center justify-center border-4 ${s.id<=stage?"border-brand-500 bg-brand-500 text-white":"border-[var(--surface-border)] bg-[var(--surface-high)] text-[var(--text-muted)]"}`}>{s.id}</div>
          <div className={`mt-1 text-sm ${s.id<=stage?"text-[var(--text-strong)]":"text-[var(--text-muted)]"}`}>{s.label}</div>
        </div>
      ))}
    </div>
  );
}
