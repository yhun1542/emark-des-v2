const API_BASE = import.meta.env.VITE_API_BASE || "";

export function startStream(question: string, onMessage:(d:any)=>void, onEnd?:()=>void) {
  const url = `/api/stream?question=${encodeURIComponent(question)}`;
  const es = new EventSource(url);
  es.onmessage = (ev) => { try { onMessage(JSON.parse(ev.data)); } catch {} };
  es.onerror = () => { es.close(); onEnd?.(); };
  return () => es.close();
}

export async function askTop(session:any, prompt?:string) {
  const res = await fetch(`/api/askTop`, {
    method:"POST", headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({ session, prompt })
  });
  return await res.json();
}
