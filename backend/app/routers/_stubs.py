"""Stub routers — will be implemented in Phase 2 (AISNP-27/28/29/30). AISNP-15"""
from fastapi import APIRouter

users_router = APIRouter(tags=["Users"])
sessions_router = APIRouter(tags=["Sessions"])
config_router = APIRouter(tags=["Config"])
db_health_router = APIRouter(tags=["DB Health"])

# Placeholder — OMEGA/ATLAS to implement in Phase 2
@users_router.get("/users/ping")
async def users_ping():
    return {"status": "users router active — full implementation in Phase 2 (AISNP-27/28)"}

@sessions_router.get("/sessions/ping")
async def sessions_ping():
    return {"status": "sessions router active — full implementation in Phase 2 (AISNP-29)"}

@config_router.get("/config")
async def get_config():
    return {"default_tickers": ["NVDA","AMD","TSM","ASML","MSFT","AVGO"],
            "stock_refresh_interval_secs": 5, "max_news_limit": 100,
            "news_query": "artificial intelligence OR semiconductor OR AI chip"}

@db_health_router.get("/db/health")
async def db_health():
    return {"status": "ok", "note": "Full DB check in Phase 2 (AISNP-30)"}
