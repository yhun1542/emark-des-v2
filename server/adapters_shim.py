import os, json, re, asyncio
from typing import Dict, Any, List, Tuple
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

ENABLE_REAL = (os.getenv("ENABLE_REAL_CALLS", "false").lower() == "true")
log.info(f"[DEBUG] ENABLE_REAL_CALLS = {os.getenv('ENABLE_REAL_CALLS', 'NOT_SET')} -> ENABLE_REAL = {ENABLE_REAL}")

try:
    from gemini_adapter import GeminiAdapter
    log.info("[DEBUG] GeminiAdapter imported successfully")
except Exception as e:
    log.warning(f"[DEBUG] Failed to import GeminiAdapter: {e}")
    GeminiAdapter = None

try:
    from grok_adapter import GrokAdapter
    log.info("[DEBUG] GrokAdapter imported successfully")
except Exception as e:
    log.warning(f"[DEBUG] Failed to import GrokAdapter: {e}")
    GrokAdapter = None

try:
    from openai_adapter import OpenAIAdapter
    log.info("[DEBUG] OpenAIAdapter imported successfully")
except Exception as e:
    log.warning(f"[DEBUG] Failed to import OpenAIAdapter: {e}")
    OpenAIAdapter = None

try:
    from claude_adapter import ClaudeAdapter
    log.info("[DEBUG] ClaudeAdapter imported successfully")
except Exception as e:
    log.warning(f"[DEBUG] Failed to import ClaudeAdapter: {e}")
    ClaudeAdapter = None

def safe_json_loads(text: str, fallback: dict) -> dict:
    """안전한 JSON 파싱 유틸리티"""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError) as e:
        log.warning(f"JSON parsing failed: {e}, text preview: {text[:200]}")
        return fallback

def get_fallback_evaluation() -> Dict[str, Any]:
    """기본 fallback 평가 구조"""
    return {
        "scores": [
            {"criterion": "feasibility", "score": 80, "reason": "fallback - 실행 가능성 평가"},
            {"criterion": "creativity", "score": 75, "reason": "fallback - 창의성 평가"},
            {"criterion": "logic", "score": 85, "reason": "fallback - 논리성 평가"},
            {"criterion": "risk", "score": 70, "reason": "fallback - 위험도 평가"},
            {"criterion": "economics", "score": 78, "reason": "fallback - 경제성 평가"}
        ],
        "notes": "fallback evaluation due to API error or parsing failure"
    }

def mock_text(tag: str) -> str:
    return f"[MOCK] {tag}\n- 핵심 요점 A\n- 핵심 요점 B\n- 핵심 요점 C"

class UnifiedAdapter:
    def __init__(self, key: str):
        self.key = key
        log.info(f"[DEBUG] Initializing UnifiedAdapter for {key}, ENABLE_REAL={ENABLE_REAL}")
        
        if ENABLE_REAL and key == "gemini" and GeminiAdapter: 
            self.ad = GeminiAdapter("Gemini 팀", "혁신적 기술 관점")
            log.info(f"[DEBUG] Created real GeminiAdapter")
        elif ENABLE_REAL and key == "grok" and GrokAdapter: 
            self.ad = GrokAdapter("Grok 팀", "실용적 현실 관점")
            log.info(f"[DEBUG] Created real GrokAdapter")
        elif ENABLE_REAL and key == "chatgpt" and OpenAIAdapter: 
            self.ad = OpenAIAdapter("ChatGPT 팀", "균형적 종합 관점")
            log.info(f"[DEBUG] Created real OpenAIAdapter")
        elif ENABLE_REAL and key == "claude" and ClaudeAdapter: 
            self.ad = ClaudeAdapter("Claude 팀", "윤리적 신중 관점")
            log.info(f"[DEBUG] Created real ClaudeAdapter")
        else: 
            self.ad = None
            log.info(f"[DEBUG] Using mock adapter for {key} (ENABLE_REAL={ENABLE_REAL})")

    def gen(self, prompt: str) -> str:
        if self.ad is None: 
            return mock_text(f"{self.key.upper()} 응답")
        
        async def _run(): 
            return await self.ad.generate_response(prompt)
        
        try: 
            return asyncio.run(_run())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(_run())
            finally:
                loop.close()
        except Exception as e:
            log.error(f"Error in gen() for {self.key}: {e}")
            return f"[ERROR] {self.key} API 호출 실패: {str(e)}"

    def team_discussion(self, question: str) -> Dict[str, Any]:
        if self.ad is None:
            leader = mock_text("Leader")
            blue = mock_text("Blue")
            research = mock_text("Research/Alternative")
            red = mock_text("Red")
            summary = mock_text("요약")
            return {
                "leader": leader,
                "blue": blue,
                "research": research,
                "red": red,
                "summary": summary
            }
        
        async def _run(): 
            return await self.ad.conduct_team_discussion(question)
        
        try:
            out = asyncio.run(_run())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                out = loop.run_until_complete(_run())
            finally:
                loop.close()
        except Exception as e:
            log.error(f"Error in team_discussion() for {self.key}: {e}")
            # 오류 발생 시 fallback 구조 반환
            return {
                "leader": f"[ERROR] {self.key} API 호출 실패: {str(e)}",
                "blue": f"[ERROR] {self.key} API 호출 실패: {str(e)}",
                "research": f"[ERROR] {self.key} API 호출 실패: {str(e)}",
                "red": f"[ERROR] {self.key} API 호출 실패: {str(e)}",
                "summary": f"[ERROR] {self.key} API 호출 실패: {str(e)}"
            }
        
        dp = out.get("discussion_process", out)
        return {
            "leader": dp.get("leader", ""),
            "blue": dp.get("blue", ""),
            "research": dp.get("alternative", ""),
            "red": dp.get("red", ""),
            "summary": out.get("final_solution", "")
        }

    def evaluate_targets(self, question: str, team_summaries: Dict[str, str]) -> Dict[str, Any]:
        """구조적으로 개선된 평가 메서드"""
        # 1차 방어선: 기본 fallback 구조 설정
        fallback_data = get_fallback_evaluation()
        
        # 평가 프롬프트 생성
        prompt = [
            "다음 요약에 대해 5개 기준으로 0~100점 채점하세요. 반드시 JSON만 반환:",
            json.dumps(team_summaries, ensure_ascii=False),
            "스키마: {\"scores\":[{\"criterion\":\"feasibility|creativity|logic|risk|economics\",\"score\":0-100,\"reason\":\"...\"},...],\"notes\":\"...\"}"
        ]
        
        # API 호출
        try:
            text = self.gen("\n".join(prompt))
        except Exception as e:
            log.error(f"API call failed in evaluate_targets for {self.key}: {e}")
            return fallback_data
        
        # 응답 검증 및 파싱
        if not text or not text.strip():
            log.warning(f"Empty response from {self.key} in evaluate_targets")
            return fallback_data
        
        # 오류 메시지 체크
        if text.startswith("[ERROR]"):
            log.warning(f"Error response from {self.key}: {text[:200]}")
            return fallback_data
        
        # JSON 구조 기본 검증
        text_stripped = text.strip()
        if not (text_stripped.startswith("{") and text_stripped.endswith("}")):
            log.warning(f"Non-JSON response from {self.key}: {text[:200]}")
            
            # 정규식으로 JSON 부분 추출 시도 (기존 로직 유지)
            m = re.search(r"\{[\s\S]*\}$", text_stripped)
            if m:
                text_stripped = m.group(0)
                log.info(f"Extracted JSON from response: {text_stripped[:100]}")
            else:
                log.warning(f"No JSON found in response from {self.key}")
                return fallback_data
        
        # 안전한 JSON 파싱
        data = safe_json_loads(text_stripped, fallback_data)
        
        # 파싱된 데이터 구조 검증
        if not isinstance(data, dict):
            log.warning(f"Invalid data structure from {self.key}: {type(data)}")
            return fallback_data
        
        # 필수 필드 검증
        if "scores" not in data or not isinstance(data["scores"], list):
            log.warning(f"Missing or invalid 'scores' field from {self.key}")
            data["scores"] = fallback_data["scores"]
        
        if "notes" not in data:
            data["notes"] = fallback_data["notes"]
        
        log.info(f"Successfully parsed evaluation from {self.key}")
        return data

def get_providers():
    return [
        UnifiedAdapter("gemini"), 
        UnifiedAdapter("grok"), 
        UnifiedAdapter("chatgpt"), 
        UnifiedAdapter("claude")
    ]

