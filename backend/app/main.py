"""
AI-SNAPSHOT FastAPI Application — Phase 2 complete
All routes wired. AISNP-15 · AISNP-20 · Owner: OMEGA
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.limiter import init_limiter
from app.routers import news, stocks, countries, health, dbhealth, config
from app.routers import users, sessions, preferences


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="AI-SNAPSHOT API",
    description="Real-time AI news and financial intelligence dashboard",
    version="1.0.0",
    lifespan=lifespan,
)

init_limiter(app)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:8765"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,       prefix="/api")
app.include_router(news.router,         prefix="/api")
app.include_router(stocks.router,       prefix="/api")
app.include_router(countries.router,    prefix="/api")
app.include_router(users.router,        prefix="/api")
app.include_router(preferences.router,  prefix="/api")
app.include_router(sessions.router,     prefix="/api")
app.include_router(config.router,       prefix="/api")
app.include_router(dbhealth.router,     prefix="/api")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
