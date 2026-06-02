from fastapi import APIRouter
router = APIRouter(tags=["Config"])
@router.get("/config")
async def get_config():
    return {"default_tickers": ["NVDA","AMD","TSM","ASML","MSFT","AVGO"],
            "stock_refresh_interval_secs": 5, "max_news_limit": 100}
