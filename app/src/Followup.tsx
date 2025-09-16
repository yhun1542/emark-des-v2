import React from "react";
import { askTop } from "./lib/api";

export default function Followup({ session }:{ session:any }){
  const top = session?.finalRanking?.[0]?.model?.toUpperCase();
  const [prompt, setPrompt] = React.useState<string>("");
  const [answer, setAnswer] = React.useState<string>("");

  React.useEffect(()=>{
    if (!session) return;
    const t = session.teams.find((x:any)=>x.model===session.finalRanking[0].model);
    const p = [
      "당신은 상위 1% 시니어 컨설턴트입니다.",
      `원질문: ${session.question}`,
      "",
      "아래는 이전 토론의 팀별 산출물 요약입니다.",
      `- Leader: ${String(t.leader).slice(0,600)}`,
      `- Blue: ${String(t.blue).slice(0,600)}`,
      `- Research: ${String(t.research).slice(0,600)}`,
      `- Red: ${String(t.red).slice(0,600)}`,
      "",
      "요구사항:",
      "1) 실행계획 30/60/90일 로드맵",
      "2) 리스크 매트릭스(발생확률×영향)와 완화전략",
      "3) KPI 8개와 데이터 소스",
      "4) 대체 시나리오 2개(A/B)와 전환 조건",
      "응답은 마크다운 표와 목록을 적극 활용하세요."
    ].join("\\n");
    setPrompt(p);
  }, [session]);

  return (
    <section className="card p-4">
      <div className="flex items-center justify-between mb-2"><div className="font-semibold">최고 점수 모델({top}) 심화 프롬프트</div>
        <button className="btn" onClick={()=>setPrompt("")}>초기화</button>
      </div>
      <textarea className="w-full h-40 rounded-lg border border-[var(--surface-border)] bg-[var(--surface-high)] p-3 outline-none" value={prompt} onChange={e=>setPrompt(e.target.value)} />
      <div className="flex items-center justify-between mt-2">
        <div className="text-xs text-[var(--text-muted)]">※ 실키 연동 시 실제 응답 반환</div>
        <button className="btn btn-primary" onClick={async()=>{ const r = await askTop(session, prompt); setAnswer(r.answer||""); }}>전송</button>
      </div>
      {Boolean(answer) && <div className="card p-3 mt-3 bg-[var(--surface-high)]"><div className="font-semibold mb-1">응답</div><div className="text-sm whitespace-pre-wrap">{answer}</div></div>}
    </section>
  );
}
