# Multi-stage build for Emark DES
FROM node:18-alpine AS frontend
WORKDIR /web

# Install dependencies
COPY app/package*.json ./
RUN npm ci --no-audit --no-fund

# Copy source and build
COPY app/ ./
RUN npm run build

# Python runtime
FROM python:3.11-slim AS runtime
WORKDIR /app

# Install Python dependencies
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server/ ./

# Copy built frontend
COPY --from=frontend /web/dist ./static

# Environment
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Run server
CMD ["sh", "-c", "gunicorn -k gevent -w ${WORKERS:-1} --access-logfile - --error-logfile - -t 0 -b 0.0.0.0:${PORT} app:app"]

