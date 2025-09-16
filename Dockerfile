# 1) Frontend build
FROM node:18-alpine AS webbuild
WORKDIR /web
ARG CACHE_BUST=20250916-1427-FORCE-DEPLOY
RUN echo "CACHE_BUST=${CACHE_BUST}" && echo "FORCE_DEPLOY_TRIGGER=${CACHE_BUST}" && date
COPY app/package*.json ./
RUN npm ci --no-audit --no-fund || npm i --no-audit --no-fund
COPY app/ ./

# Debug: 빌드 컨텍스트 점검
RUN echo "--- Web stage tree ---" && ls -la && \
    echo "--- src ---" && ls -la src || true && \
    echo "--- src/lib ---" && ls -la src/lib || true && \
    echo "--- App.tsx head ---" && head -n 20 src/App.tsx || true

RUN npm run build

# 2) Python runtime
FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ARG CACHE_BUST=20250916-1427-FORCE-DEPLOY
RUN echo "PYTHON_CACHE_BUST=${CACHE_BUST}" && echo "FORCE_DEPLOY_TRIGGER=${CACHE_BUST}" && date
WORKDIR /app
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server/ ./ 
# Frontend dist → Flask static
COPY --from=webbuild /web/dist ./static

# Gunicorn: PORT 환경변수 치환(쉘 실행)
CMD ["sh","-c","gunicorn -k gevent -w ${WORKERS:-1} --access-logfile - --error-logfile - -t 0 -b 0.0.0.0:${PORT} app:app"]

