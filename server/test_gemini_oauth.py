import os
import asyncio
from dotenv import load_dotenv
from gemini_adapter import GeminiAdapter

# 환경변수 로드
load_dotenv()

async def test_gemini_oauth():
    print("=== OAuth2 기반 Gemini 어댑터 테스트 ===")
    
    # 환경변수 확인
    print(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID', 'NOT SET')}")
    print(f"GOOGLE_CLIENT_SECRET: {os.getenv('GOOGLE_CLIENT_SECRET', 'NOT SET')[:20]}...")
    print(f"GOOGLE_REFRESH_TOKEN: {os.getenv('GOOGLE_REFRESH_TOKEN', 'NOT SET')[:20]}...")
    
    # Gemini 어댑터 생성
    adapter = GeminiAdapter("테스트팀", "기술적 관점")
    
    # 간단한 질문 테스트
    print("\n=== 간단한 질문 테스트 ===")
    response = await adapter.generate_response("안녕하세요! 간단한 인사말을 해주세요.")
    print(f"응답: {response}")
    
    print("\n테스트 완료!")

if __name__ == "__main__":
    asyncio.run(test_gemini_oauth())

