# Emark DES - AI API 오류 로그 상세 분석

## 현재 상태 요약 (2025-09-16 11:14 기준)

### ✅ 정상 작동 중인 API
- **ChatGPT (OpenAI)**: 완전히 정상 작동, 모든 역할(Leader, Blue, Research, Red)에서 상세한 응답 생성
- **Claude (Anthropic)**: 정상 작동, 모든 역할에서 응답 생성 완료

### ❌ 오류 발생 중인 API

## 1. Gemini API 오류

**오류 메시지:**
```
[ERROR] Gemini API 호출 실패: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.
```

**발생 위치:** 모든 역할 (Leader, Blue, Research, Red, 리더 요약)

**원인 분석:**
- 모델명 `gemini-pro`가 더 이상 지원되지 않음
- Google AI Studio에서 모델명이 `gemini-1.5-flash` 또는 `gemini-1.5-pro`로 변경됨

**해결 방법:**
```python
# gemini_adapter.py에서 수정 필요
self.model = "gemini-1.5-flash"  # 또는 "gemini-1.5-pro"
```

## 2. Grok API 오류

**오류 메시지:**
```
[ERROR] Grok API 호출 실패: unknown enum label "system"
```

**발생 위치:** 모든 역할 (Leader, Blue, Research, Red, 리더 요약)

**원인 분석:**
- Grok API에서 `system` 역할을 지원하지 않음
- 메시지 형식에서 system 역할 사용 시 오류 발생

**해결 방법:**
```python
# grok_adapter.py에서 수정 필요
# system 역할을 user 메시지에 포함시키거나 제거
messages = [
    {"role": "user", "content": f"당신은 {self.team_name}입니다. {self.perspective}에서 답변해주세요.\n\n{prompt}"}
]
```

## 3. OpenAI API 연결 오류 (로컬 테스트에서 발견)

**오류 메시지:**
```
OpenAI API Error: httpx.UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol.
```

**원인 분석:**
- `OPENAI_API_BASE` 환경 변수가 잘못 설정되었거나 비어있음
- URL 프로토콜이 누락됨

**해결 방법:**
```python
# openai_adapter.py에서 수정 필요
self.client = openai.AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")  # 기본값 설정
)
```

## 실제 테스트 결과

### ChatGPT 응답 예시 (정상 작동)
```
Leader: 1. **혁신적인 아이디어**: 스타트업은 종종 새로운 시장을 창출하거나 기존 시장을 방해하는 혁신적인 제품이나 서비스를 개발합니다...

Blue: 스타트업의 성공을 위한 핵심 전략은 여러 가지가 있지만, 여기서는 몇 가지 핵심적인 전략에 대해 긍정적인 측면과 기회요소를 탐색해 보겠습니다...

Research: 스타트업 성공을 위한 전략은 다양하게 제시되고 있지만, 대안적 접근방법을 통해 필요한 몇 가지 핵심 전략을 제시하겠습니다...

Red: 스타트업의 성공을 위한 전략은 다양하며, 이는 그 스타트업의 특성, 목표, 시장 환경 등에 따라 달라집니다...
```

### Claude 응답 예시 (정상 작동)
```
Leader: 스타트업의 성공을 위한 핵심 전략은 혁신적인 아이디어, 명확한 실행 가능한 비즈니스 모델, 다양한 스킬과 경험을 갖춘 강력한 팀...

Blue: 스타트업의 성공을 위한 핵심 전략들은 여러 가지가 있지만, 여기서는 몇 가지 핵심적인 전략에 대해 긍정적인 측면과 기회요소를 탐색해 보겠습니다...
```

## 우선순위 수정 사항

1. **Gemini 모델명 수정** (높음) - 간단한 문자열 변경으로 해결 가능
2. **Grok system 역할 제거** (높음) - 메시지 형식 수정 필요
3. **OpenAI base URL 검증** (중간) - 환경 변수 확인 및 기본값 설정

## 현재 시스템 안정성

- **전체 시스템**: 정상 작동 (fallback 메커니즘으로 인해 오류 발생 시에도 중단되지 않음)
- **실시간 스트리밍**: 정상 작동
- **UI/UX**: 정상 작동
- **Railway 배포**: 안정적

