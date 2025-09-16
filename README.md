# Emark DES - AI Discussion & Evaluation System

AI 모델들이 주제에 대해 토론하고 상호 평가하는 시스템입니다.

## 🚀 Features

- **4개 AI 모델 토론**: GPT-4, Claude, Gemini, Grok
- **실시간 SSE 스트리밍**: 토론 과정 실시간 확인  
- **상호 교차 평가**: AI들이 서로를 평가
- **시각화**: 레이더 차트, 매트릭스, 순위 시스템
- **반응형 UI**: React + TypeScript

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Vite, Chart.js
- **Backend**: Flask, Server-Sent Events (SSE)
- **Deployment**: Docker, Railway

## 🏃‍♂️ Quick Start

### Local Development

```bash
# Install dependencies
make install

# Build and run
make run
```

### Docker

```bash
# Build image
make docker-build

# Run container
make docker-run
```

## 🌍 Environment Variables

```env
ENABLE_REAL_CALLS=false          # true for real AI APIs
OPENAI_API_KEY=your_key_here     # GPT-4
ANTHROPIC_API_KEY=your_key_here  # Claude  
GEMINI_API_KEY=your_key_here     # Gemini
XAI_API_KEY=your_key_here        # Grok
WORKERS=1                        # Gunicorn workers
```

## 📡 API Endpoints

- `GET /health` - Health check
- `GET /api/stream?question=<topic>` - Start discussion (SSE)
- `POST /api/askTop` - Follow-up questions

## 🎯 Usage

1. 웹 인터페이스에서 토론 주제 입력
2. 4개 AI 모델이 각각 4가지 역할로 토론 진행
3. 실시간으로 토론 과정 확인
4. 상호 평가 결과 및 최종 순위 확인
5. 상세 분석 및 심화 질문 가능

