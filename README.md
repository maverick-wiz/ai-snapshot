# AI-SNAPSHOT

> Real-time AI & Financial Intelligence Dashboard

[![CI](https://github.com/maverick-wiz/ai-snapshot/actions/workflows/ci.yml/badge.svg)](https://github.com/maverick-wiz/ai-snapshot/actions/workflows/ci.yml)

## Stack

| Layer | Technology |
|---|---|
| Frontend | ReactJS 18 + Vite 5 + TypeScript |
| Backend | Python FastAPI + uvicorn |
| News | Google News RSS (feedparser) |
| Stocks | yfinance (Yahoo Finance) |
| Database | PostgreSQL 15 + SQLAlchemy 2.0 + Alembic |
| K8s | Minikube (AI-SNAPSHOT-KLUSTER profile) |
| CI/CD | GitHub Actions (5-stage pipeline) |

## Jira Board

[AI-SNAPSHOT Board (AISNP)](https://wizkidtester.atlassian.net/jira/software/projects/AISNP/boards/34)

## Quick Start (Local Dev)

```bash
# 1. Clone
git clone https://github.com/maverick-wiz/ai-snapshot.git
cd ai-snapshot

# 2. Copy env
cp .env.example .env.local
# Edit .env.local with your DATABASE_URL etc.

# 3. Start services
docker compose up -d

# 4. Run migrations
cd backend && alembic upgrade head

# 5. Start frontend (separate terminal)
cd frontend && npm install && npm run dev

# App: http://localhost:5173 (dev) or http://localhost:8765 (prod build)
```

## Project Structure

```
ai-snapshot/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py       # App entry point
│   │   ├── routers/      # API route handlers
│   │   ├── models.py     # SQLAlchemy ORM models
│   │   ├── schemas.py    # Pydantic v2 schemas
│   │   ├── db.py         # Async DB engine + session
│   │   ├── cache.py      # In-memory TTL cache
│   │   └── gbm.py        # GBM stock fallback
│   ├── migrations/   # Alembic migrations
│   ├── tests/        # pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # Vite + React + TypeScript
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks (useStocks, useNews)
│   │   ├── api/          # API client functions
│   │   ├── types/        # TypeScript interfaces
│   │   └── styles/       # Global CSS
│   └── package.json
├── k8s/              # Kubernetes manifests
│   ├── namespace.yaml
│   ├── backend/      # Deployment, Service, ConfigMap
│   ├── postgres/     # StatefulSet, PVC, Service
│   └── ingress.yaml
├── .github/
│   └── workflows/
│       └── ci.yml    # 5-stage CI/CD pipeline
└── docker-compose.yml
```

## Team

| Agent | Role | Jira Epic |
|---|---|---|
| ALPHA | DevOps / K8s | [AISNP-1](https://wizkidtester.atlassian.net/browse/AISNP-1) |
| OMEGA | Backend API | [AISNP-2](https://wizkidtester.atlassian.net/browse/AISNP-2) |
| PIXEL | Frontend UI | [AISNP-3](https://wizkidtester.atlassian.net/browse/AISNP-3) |
| ATLAS | Database | [AISNP-6](https://wizkidtester.atlassian.net/browse/AISNP-6) |
| DELTA | QA | [AISNP-5](https://wizkidtester.atlassian.net/browse/AISNP-5) |
| SAGE | Code Review | All PRs |
