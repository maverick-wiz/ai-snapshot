"""
AI-SNAPSHOT FastAPI Application
AISNP-15 · Owner: OMEGA
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import news, stocks, countries, users, sessions, config, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="AI-SNAPSHOT API",
    description="Real-time AI news and financial intelligence dashboard",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:8765").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(health.router, prefix="/api")
app.include_router(news.router, prefix="/api")
app.include_router(stocks.router, prefix="/api")
app.include_router(countries.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(config.router, prefix="/api")

# Serve React build at / (production only — when dist/ exists)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
