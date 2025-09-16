import React from "react";
import { Radar, Bar } from "react-chartjs-2";
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from "chart.js";
ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

export default function LazyCharts({ final }:{ final:any }){
  const labels = final?.finalRanking?.[0]?.breakdown?.map((b:any)=>b.criterion) ?? [];
  const ds = (model:string) => final?.finalRanking?.find((fr:any)=>fr.model===model)?.breakdown?.map((b:any)=>b.score) ?? [];
  const datasets = final?.finalRanking?.map((fr:any)=>({ label: fr.model.toUpperCase(), data: ds(fr.model), fill:true, borderWidth:2, pointRadius:2 })) ?? [];
  return (
    <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div className="card p-4"><div className="font-semibold mb-2">항목별 평균 점수 (Radar)</div><Radar data={{ labels, datasets }} /></div>
      <div className="card p-4"><div className="font-semibold mb-2">최종 평균 점수 (Bar)</div><Bar data={{ labels: final?.finalRanking?.map((fr:any)=>fr.model.toUpperCase()), datasets:[{ label:"평균점", data: final?.finalRanking?.map((fr:any)=>fr.total) }]}} options={{ scales:{ y:{ suggestedMin:0, suggestedMax:100 }}}} /></div>
    </section>
  );
}
