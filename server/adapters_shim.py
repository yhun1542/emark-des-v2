#!/usr/bin/env python3
"""
EmarkOS Adapter Shim - Final Safe Implementation
- 안전한 JSON 파싱 및 fallback 지원
- JSONDecodeError로 서버가 죽지 않음
"""

import os
import json
import re
import asyncio
import logging
from typing import Dict, Any, List, Tuple

# 로깅 설정
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

ENABLE_REAL = (os.getenv("ENABLE_REAL_CALLS", "false").lower() == "true")
log.info(f"[SHIM] ENABLE_REAL_CALLS = {os.getenv('ENABLE_REAL_CALLS', 'NOT_SET')} -> {ENABLE_REAL}")

# 어댑터 import 시도
try:
    from gemini_adapter import GeminiAdapter
    log.info("[SHIM] GeminiAdapter imported successfully")
except Exception as e:
    log.warning(f"[SHIM] Failed to import GeminiAdapter: {e}")
    GeminiAdapter = None

try:
    from grok_adapter import GrokAdapter
    log.info("[SHIM] GrokAdapter imported successfully")
except Exception as e:
    log.warning(f"[SHIM] Failed to import GrokAdapter: {e}")
    GrokAdapter = None

try:
    from openai_adapter import OpenAIAdapter
    log.info("[SHIM] OpenAIAdapter imported successfully")
except Exception as e:
    log.warning(f"[SHIM] Failed to import OpenAIAdapter: {e}")
    OpenAIAdapter = None

try:
    from claude_adapter import ClaudeAdapter
    log.info("[SHIM] ClaudeAdapter imported successfully")
except Exception as e:
    log.warning(f"[SHIM] Failed to import ClaudeAdapter: {e}")
    ClaudeAdapter = None

def safe_json_parse(text: str) -> Dict[str, Any]:
    """
    안전한 JSON 파싱 - 핵심 함수
    """
    # fallback 기본 구조
    fallback = {
        "scores": [
            {"criterion": "feasibility", "score": 80, "reason": "fallback - 실행 가능성"},
            {"criterion": "creativity", "score": 75, "reason": "fallback - 창의성"},
            {"criterion": "logic", "score": 85, "reason": "fallback - 논리성"},
            {"criterion": "risk", "score": 70, "reason": "fallback - 위험도"},
            {"criterion": "economics", "score": 78, "reason": "fallback - 경제성"}
        ],
        "notes": "safe fallback due to JSON parsing failure"
    }

    # 1. 응답 비었을 경우
    if not text or not text.strip():
        log.warning("[SHIM] empty response, using fallback")
        return fallback

    stripped = text.strip()

    # 2. JSON 응답으로 보이는 경우만 파싱
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            result = json.loads(stripped)
            log.info("[SHIM] JSON parsing successful")
            return result
        except json.JSONDecodeError as e:
            log.warning(f"[SHIM] JSON parsing failed: {e}, text: {stripped[:200]}")
            return fallback

    # 3. 정규식으로 JSON 부분 추출 시도 (기존 로직 유지)
    json_match = re.search(r'\{[\s\S]*\}$', stripped)
    if json_match:
        try:
            result = json.loads(json_match.group(0))
            log.info("[SHIM] JSON extraction and parsing successful")
            return result
        except json.JSONDecodeError as e:
            log.warning(f"[SHIM] Extracted JSON parsing failed: {e}")
            return fallback

    # 4. JSON이 아닐 경우 fallback
    log.warning(f"[SHIM] non-JSON response, using fallback. text: {stripped[:200]}")
    return fallback

def mock_text(tag: str) -> str:
    """Mock 텍스트 생성"""
    return f"[MOCK] {tag}\n- 핵심 요점 A\n- 핵심 요점 B\n- 핵심 요점 C"

class UnifiedAdapter:
    """통합 어댑터 - 안전한 구현"""
    
    def __init__(self, key: str):
        self.key = key
        log.info(f"[SHIM] Initializing UnifiedAdapter for {key}")
        
        # 실제 어댑터 초기화
        if ENABLE_REAL and key == "gemini" and GeminiAdapter:
            self.ad = GeminiAdapter("Gemini 팀", "혁신적 기술 관점")
            log.info(f"[SHIM] Created real GeminiAdapter")
        elif ENABLE_REAL and key == "grok" and GrokAdapter:
            self.ad = GrokAdapter("Grok 팀", "실용적 현실 관점")
            log.info(f"[SHIM] Created real GrokAdapter")
        elif ENABLE_REAL and key == "chatgpt" and OpenAIAdapter:
            self.ad = OpenAIAdapter("ChatGPT 팀", "균형적 종합 관점")
            log.info(f"[SHIM] Created real OpenAIAdapter")
        elif ENABLE_REAL and key == "claude" and ClaudeAdapter:
            self.ad = ClaudeAdapter("Claude 팀", "윤리적 신중 관점")
            log.info(f"[SHIM] Created real ClaudeAdapter")
        else:
            self.ad = None
            log.info(f"[SHIM] Using mock adapter for {key}")

    def gen(self, prompt: str) -> str:
        """텍스트 생성 - 안전한 구현"""
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
            log.error(f"[SHIM] Error in gen() for {self.key}: {e}")
            return f"[ERROR] {self.key} API 호출 실패: {str(e)}"

    def team_discussion(self, question: str) -> Dict[str, Any]:
        """팀 토론 - 안전한 구현"""
        if self.ad is None:
            return {
                "leader": mock_text("Leader"),
                "blue": mock_text("Blue"),
                "research": mock_text("Research/Alternative"),
                "red": mock_text("Red"),
                "summary": mock_text("요약")
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
            log.error(f"[SHIM] Error in team_discussion() for {self.key}: {e}")
            error_msg = f"[ERROR] {self.key} API 호출 실패: {str(e)}"
            return {
                "leader": error_msg,
                "blue": error_msg,
                "research": error_msg,
                "red": error_msg,
                "summary": error_msg
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
        """
        타겟 평가 - 완전히 안전한 구현
        *** 핵심: JSONDecodeError로 서버가 절대 죽지 않음 ***
        """
        log.info(f"[SHIM] evaluate_targets called for {self.key}")
        
        # 평가 프롬프트 생성
        prompt = [
            "다음 요약에 대해 5개 기준으로 0~100점 채점하세요. 반드시 JSON만 반환:",
            json.dumps(team_summaries, ensure_ascii=False),
            "스키마: {\"scores\":[{\"criterion\":\"feasibility|creativity|logic|risk|economics\",\"score\":0-100,\"reason\":\"...\"},...],\"notes\":\"...\"}"
        ]
        
        # API 호출
        try:
            text = self.gen("\n".join(prompt))
            log.info(f"[SHIM] API response received for {self.key}: {text[:100]}...")
        except Exception as e:
            log.error(f"[SHIM] API call failed for {self.key}: {e}")
            return safe_json_parse("")  # 빈 문자열로 fallback 트리거
        
        # *** 핵심: 안전한 JSON 파싱 ***
        result = safe_json_parse(text)
        log.info(f"[SHIM] evaluate_targets completed for {self.key}")
        return result

def get_providers():
    """프로바이더 목록 반환"""
    return [
        UnifiedAdapter("gemini"),
        UnifiedAdapter("grok"), 
        UnifiedAdapter("chatgpt"),
        UnifiedAdapter("claude")
    ]

