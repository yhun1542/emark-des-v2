import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
            "grant_type": "refresh_token"
        }
    )
    resp.raise_for_status()
    return resp.json()

def check_token_info(access_token):
    resp = requests.get(
        f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}"
    )
    return resp.json()

# 토큰 정보 확인
print("=== OAuth2 토큰 정보 확인 ===")
token_data = get_access_token()
print(f"Token response: {token_data}")

access_token = token_data["access_token"]
token_info = check_token_info(access_token)
print(f"Token info: {token_info}")

# Generative AI API 엔드포인트 테스트
print("\n=== API 엔드포인트 테스트 ===")
headers = {"Authorization": f"Bearer {access_token}"}

# 1. 모델 목록 조회
try:
    resp = requests.get(
        "https://generativelanguage.googleapis.com/v1beta/models",
        headers=headers
    )
    print(f"Models list status: {resp.status_code}")
    if resp.status_code == 200:
        models = resp.json()
        print(f"Available models: {[m.get('name', 'unknown') for m in models.get('models', [])]}")
    else:
        print(f"Models list error: {resp.text}")
except Exception as e:
    print(f"Models list exception: {e}")

# 2. 간단한 생성 테스트
try:
    payload = {
        "contents": [
            {"parts": [{"text": "Hello"}]}
        ]
    }
    resp = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        headers=headers,
        json=payload
    )
    print(f"Generate content status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Generate content success: {resp.json()}")
    else:
        print(f"Generate content error: {resp.text}")
except Exception as e:
    print(f"Generate content exception: {e}")

