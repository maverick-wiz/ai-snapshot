# Build stage: compile React frontend
FROM node:20-slim AS frontend-builder
WORKDIR /frontend
COPY ../frontend/package*.json ./
RUN npm ci
COPY ../frontend/ .
ENV VITE_API_URL=/api
RUN npm run build

# Runtime stage: FastAPI + built React
FROM python:3.11-slim AS runtime
WORKDIR /app

RUN useradd -m -u 1001 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY --from=frontend-builder /frontend/dist/ ./static/

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8765
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8765", "--workers", "2"]
