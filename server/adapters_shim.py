import os, json, re, asyncio
from typing import Dict, Any, List, Tuple

ENABLE_REAL = (os.getenv("ENABLE_REAL_CALLS", "false").lower() == "true")

try:
    from gemini_adapter import GeminiAdapter
    from grok_adapter import GrokAdapter
    from openai_adapter import OpenAIAdapter
    from claude_adapter import ClaudeAdapter
except Exception:
    GeminiAdapter = GrokAdapter = OpenAIAdapter = ClaudeAdapter = None

def mock_text(tag: str) -> str:
    return f"[MOCK] {tag}\n- 핵심 요점 A\n- 핵심 요점 B\n- 핵심 요점 C"

class UnifiedAdapter:
    def __init__(self, key:str):
        self.key = key
        if ENABLE_REAL and key=="gemini" and GeminiAdapter: self.ad = GeminiAdapter("Gemini 팀","혁신적 기술 관점")
        elif ENABLE_REAL and key=="grok" and GrokAdapter: self.ad = GrokAdapter("Grok 팀","실용적 현실 관점")
        elif ENABLE_REAL and key=="chatgpt" and OpenAIAdapter: self.ad = OpenAIAdapter("ChatGPT 팀","균형적 종합 관점")
        elif ENABLE_REAL and key=="claude" and ClaudeAdapter: self.ad = ClaudeAdapter("Claude 팀","윤리적 신중 관점")
        else: self.ad = None

    def gen(self, prompt:str) -> str:
        if self.ad is None: return mock_text(f"{self.key.upper()} 응답")
        async def _run(): return await self.ad.generate_response(prompt)
        try: return asyncio.run(_run())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(_run())
            finally:
                loop.close()

    def team_discussion(self, question:str) -> Dict[str, Any]:
        if self.ad is None:
            leader = mock_text("Leader"); blue = mock_text("Blue")
            research = mock_text("Research/Alternative"); red = mock_text("Red")
            summary = mock_text("요약")
            return {"leader":leader,"blue":blue,"research":research,"red":red,"summary":summary}
        async def _run(): return await self.ad.conduct_team_discussion(question)
        try:
            out = asyncio.run(_run())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                out = loop.run_until_complete(_run())
            finally:
                loop.close()
        dp = out.get("discussion_process", out)
        return {
            "leader": dp.get("leader",""),
            "blue": dp.get("blue",""),
            "research": dp.get("alternative",""),
            "red": dp.get("red",""),
            "summary": out.get("final_solution","")
        }

    def evaluate_targets(self, question:str, team_summaries: Dict[str,str]) -> Dict[str, Any]:
        prompt = [
            "다음 요약에 대해 5개 기준으로 0~100점 채점하세요. 반드시 JSON만 반환:",
            json.dumps(team_summaries, ensure_ascii=False),
            "스키마: {\"scores\":[{\"criterion\":\"feasibility|creativity|logic|risk|economics\",\"score\":0-100,\"reason\":\"...\"},...],\"notes\":\"...\"}"
        ]
        text = self.gen("\n".join(prompt))
        try:
            data = json.loads(text)
        except Exception:
            m = re.search(r"\{[\s\S]*\}$", text.strip())
            data = json.loads(m.group(0)) if m else {"scores":[{"criterion":"feasibility","score":80,"reason":"mock"}], "notes":"mock"}
        return data

def get_providers():
    return [UnifiedAdapter("gemini"), UnifiedAdapter("grok"), UnifiedAdapter("chatgpt"), UnifiedAdapter("claude")]
