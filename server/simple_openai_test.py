#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import openai

load_dotenv()

def test_openai_sync():
    try:
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "안녕하세요, 간단한 테스트입니다."}
            ],
            max_tokens=50
        )
        
        print("OpenAI API 테스트 성공!")
        print("응답:", response.choices[0].message.content)
        return True
    except Exception as e:
        print(f"OpenAI API 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    test_openai_sync()

