export type ModelKey = "gemini" | "grok" | "chatgpt" | "claude";
export type DebateRole = "leader" | "blue" | "research" | "red";
export interface DebateMessage { role: DebateRole; content: string; }
export interface TeamState {
  model: ModelKey; status:"idle"|"running"|"done"; progress:number;
  leader?: DebateMessage; blue?: DebateMessage; research?: DebateMessage; red?: DebateMessage; summary?: string;
}
export interface EvalItem {
  evaluator: ModelKey; target: ModelKey; total: number;
  scores: { criterion:string; score:number; reason:string }[]; notes?: string;
}
