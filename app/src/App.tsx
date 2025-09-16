import React from "react";
import "./styles.css";
import { startStream } from "./lib/api";
import Stepper from "./components/Stepper";
import TeamGrid from "./components/TeamGrid";
import Matrix from "./components/Matrix";
import DetailModal from "./components/DetailModal";
import Followup from "./Followup";
import type { TeamState, EvalItem, ModelKey } from "./types";

const LazyCharts = React.lazy(()=>import("./lazyCharts"));

export default function App(){
  const [question, setQuestion] = React.useState("");
  const [stage, setStage] = React.useState<1|2|3>(1);
  const base: TeamState[] = [
    { model:"gemini", status:"idle", progress:0 },
    { model:"grok", status:"idle", progress:0 },
    { model:"chatgpt", status:"idle", progress:0 },
    { model:"claude", status:"idle", progress:0 }
  ];
  const [teams, setTeams] = React.useState<TeamState[]>(base);
  const [evals, setEvals] = React.useState<EvalItem[]>([]);
  const [final, setFinal] = React.useState<any>(null);
  const [detail, setDetail] = React.useState<ModelKey|null>(null);
  const [running, setRunning] = React.useState(false);
  const [log, setLog] = React.useState<string[]>([]);

  function pushLog(s:string){ setLog(prev => [...prev.slice(-80), s]); }

  function onMsg(d:any){
    if (d.type==="session.start"){ setRunning(true); pushLog("세션 시작"); }
    if (d.type==="team.start"){ setTeams(ts=>ts.map(t=>t.model===d.model?{...t,status:"running"}:t)); }
    if (d.type==="role.done"){ setTeams(ts=>ts.map(t=>{
      if (t.model!==d.model) return t;
      const p = Math.min(100, t.progress+20);
      return { ...t, progress:p, [d.role]: d.message };
    })); pushLog(`${d.model.toUpperCase()} — ${d.role} 완료`); }
    if (d.type==="team.summary"){ setTeams(ts=>ts.map(t=>t.model===d.model?{...t, summary:d.summary}:t)); }
    if (d.type==="team.done"){ setTeams(ts=>ts.map(t=>t.model===d.model?{...t, status:"done", progress:100}:t)); }
    if (d.type==="stage.done"){ setStage(d.stage); }
    if (d.type==="evaluation.done"){ setEvals(es=>[...es, d.evaluation]); }
    if (d.type==="final"){ setFinal(d.session); setRunning(false); pushLog("최종 집계 완료"); setStage(3); }
  }

  function run(){
    setTeams(base); setEvals([]); setFinal(null); setStage(1); setLog([]);
    startStream(question, onMsg, ()=>setRunning(false));
  }

  return (
    <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      <section className="card p-4">
        <div className="text-sm text-[var(--text-muted)] mb-1">토론 안건</div>
        <textarea className="w-full h-28 rounded-lg border border-[var(--surface-border)] bg-[var(--surface-high)] p-3 outline-none" value={question} onChange={e=>setQuestion(e.target.value)} placeholder="예) 중소형 개발사의 12개월 프로젝트 리스크/ROI 최적화 전략은?" />
        <div className="flex items-center justify-between mt-2">
          <span className="text-xs text-[var(--text-muted)]">SSE로 실시간 진행상황 표시</span>
          <button className="btn btn-primary" disabled={!question.trim()||running} onClick={run}>실행</button>
        </div>
      </section>

      <section className="card p-4">
        <Stepper stage={stage} />
        <TeamGrid teams={teams} />
        <div className="card p-3 bg-[var(--surface-high)] mt-3">
          <div className="text-sm font-semibold mb-1">실시간 로그</div>
          <div className="text-xs max-h-40 overflow-y-auto space-y-1">{log.map((s,i)=>(<div key={i} className="text-[var(--text-muted)]">{s}</div>))}</div>
        </div>
      </section>

      {final && (
        <section className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
            {final.finalRanking.map((fr:any, idx:number)=>(
              <div key={fr.model} className={`card p-4 ${idx===0?"ring-2 ring-brand-600":""}`}>
                <div className="flex items-center justify-between mb-2"><div className="text-xs text-[var(--text-muted)]">Rank {idx+1}</div><div className="badge">{fr.model.toUpperCase()}</div></div>
                <div className="text-3xl font-bold">{fr.total}</div>
                <div className="text-xs text-[var(--text-muted)] mt-1">가중 종합점</div>
                <button className="btn mt-3 w-full" onClick={()=>setDetail(fr.model)}>상세보기</button>
              </div>
            ))}
          </div>

          <div className="card p-4">
            <div className="font-semibold mb-2">AI 교차 평가 매트릭스</div>
            <Matrix evals={evals} />
          </div>

          <React.Suspense fallback={<div className="card p-6 skeleton h-60 rounded" />}>
            <LazyCharts final={final} />
          </React.Suspense>
        </section>
      )}

      {final && <Followup session={final} />}

      <DetailModal open={!!detail} onClose={()=>setDetail(null)} model={detail as ModelKey} evals={evals} team={final?.teams.find((t:any)=>t.model===detail)} />
    </main>
  );
}
