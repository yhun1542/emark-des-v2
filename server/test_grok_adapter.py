import os
import asyncio
from dotenv import load_dotenv
from grok_adapter import GrokAdapter

load_dotenv()

async def test_grok_adapter():
    print("=== Grok 어댑터 테스트 ===")
    
    # 환경변수 확인
    api_key = os.getenv("XAI_API_KEY", "")
    print(f"XAI_API_KEY: {api_key[:20] if api_key else 'NOT SET'}...")
    
    if not api_key:
        print("XAI_API_KEY가 설정되지 않았습니다.")
        return
    
    # Grok 어댑터 생성
    adapter = GrokAdapter("테스트팀", "기술적 관점")
    
    # 간단한 질문 테스트
    print("\n=== 간단한 질문 테스트 ===")
    response = await adapter.generate_response("안녕하세요! 간단한 인사말을 해주세요.")
    print(f"응답: {response}")
    
    print("\n테스트 완료!")

if __name__ == "__main__":
    asyncio.run(test_grok_adapter())

