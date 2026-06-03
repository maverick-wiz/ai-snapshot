"""GET /api/config public fallback (no DB required). AISNP-30"""
from fastapi import APIRouter
router = APIRouter(tags=["Config"])

@router.get("/config/public")
async def get_config_public():
    return {"default_tickers": ["NVDA","AMD","TSM","ASML","MSFT","AVGO"],
            "stock_refresh_interval_secs": 5, "max_news_limit": 100,
            "news_query": "artificial intelligence OR semiconductor OR AI chip"}
