import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

async def test_gemini_models():
    print("=== Gemini 모델명 테스트 ===")
    
    # API 키 설정
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        return
    
    genai.configure(api_key=api_key)
    print(f"API Key: {api_key[:20]}...")
    
    # 테스트할 모델명들
    model_names = [
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'gemini-pro',
        'models/gemini-1.5-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro',
        'gemini-1.5-pro-latest',
        'gemini-1.5-flash-latest'
    ]
    
    for model_name in model_names:
        print(f"\n--- 테스트 모델: {model_name} ---")
        try:
            model = genai.GenerativeModel(model_name)
            
            # 동기 방식으로 테스트
            response = model.generate_content("안녕하세요!")
            print(f"✅ 성공: {response.text[:100]}...")
            break  # 성공하면 중단
            
        except Exception as e:
            print(f"❌ 실패: {str(e)}")
    
    print("\n=== 사용 가능한 모델 목록 조회 ===")
    try:
        models = genai.list_models()
        print("사용 가능한 모델들:")
        for model in models:
            if 'gemini' in model.name.lower():
                print(f"  - {model.name}")
    except Exception as e:
        print(f"모델 목록 조회 실패: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini_models())

