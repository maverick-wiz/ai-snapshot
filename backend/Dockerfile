# Multi-stage Dockerfile — AISNP-22 · Owner: OMEGA
# Stage 1: Build React frontend
FROM node:20-slim AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci --silent
COPY frontend/ .
ENV VITE_API_URL=/api
RUN npm run build

# Stage 2: FastAPI runtime with built React
FROM python:3.11-slim AS runtime
WORKDIR /app

# Non-root user
RUN useradd -m -u 1001 appuser

# Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY backend/app/ ./app/
COPY backend/migrations/ ./migrations/
COPY backend/alembic.ini .

# React build from Stage 1
COPY --from=frontend-builder /frontend/dist/ ./static/

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8765

# Run migrations then start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8765 --workers 2"]
