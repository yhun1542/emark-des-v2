#!/usr/bin/env python3
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_openai():
    try:
        from openai_adapter import OpenAIAdapter
        adapter = OpenAIAdapter("ChatGPT 팀", "균형적 종합 관점")
        result = await adapter.generate_response("안녕하세요, 간단한 테스트입니다.")
        print("OpenAI 테스트 성공:")
        print(result[:200] + "..." if len(result) > 200 else result)
        return True
    except Exception as e:
        print(f"OpenAI 테스트 실패: {e}")
        return False

async def test_gemini():
    try:
        from gemini_adapter import GeminiAdapter
        adapter = GeminiAdapter("Gemini 팀", "혁신적 기술 관점")
        result = await adapter.generate_response("안녕하세요, 간단한 테스트입니다.")
        print("Gemini 테스트 성공:")
        print(result[:200] + "..." if len(result) > 200 else result)
        return True
    except Exception as e:
        print(f"Gemini 테스트 실패: {e}")
        return False

async def test_adapters_shim():
    try:
        from adapters_shim import get_providers
        providers = get_providers()
        print(f"프로바이더 수: {len(providers)}")
        
        for provider in providers:
            print(f"\n{provider.key} 테스트 중...")
            result = provider.gen("안녕하세요")
            print(f"결과: {result[:100]}...")
        return True
    except Exception as e:
        print(f"Adapters shim 테스트 실패: {e}")
        return False

async def main():
    print("=== AI 어댑터 테스트 시작 ===")
    print(f"ENABLE_REAL_CALLS: {os.getenv('ENABLE_REAL_CALLS')}")
    print(f"OPENAI_API_KEY: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT_SET'}")
    print(f"GEMINI_API_KEY: {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT_SET'}")
    print()
    
    await test_openai()
    print()
    await test_gemini()
    print()
    await test_adapters_shim()

if __name__ == "__main__":
    asyncio.run(main())

