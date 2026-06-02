"""
GET /api/stocks — yfinance live prices with GBM fallback.
AISNP-18 · Owner: OMEGA
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Query
from app.schemas import StocksResponse, StockQuote
from app.cache import cache, STOCKS_TTL
from app.gbm import generate_gbm_quote, GBM_BASELINES

router = APIRouter(tags=["Stocks"])

DEFAULT_TICKERS = ["NVDA", "AMD", "TSM", "ASML", "MSFT", "AVGO"]

TICKER_NAMES = {
    "NVDA": "NVIDIA Corporation", "AMD": "Advanced Micro Devices",
    "TSM": "Taiwan Semiconductor Mfg", "ASML": "ASML Holding N.V.",
    "MSFT": "Microsoft Corporation", "AVGO": "Broadcom Inc.",
}


def _fetch_yfinance(ticker: str) -> dict:
    import yfinance as yf
    t = yf.Ticker(ticker)
    info = t.fast_info
    price = float(info.last_price or 0)
    prev = float(info.previous_close or price)
    change = round(price - prev, 2)
    change_pct = round((change / prev) * 100, 2) if prev else 0.0
    volume = int(info.three_month_average_volume or 0)
    return {
        "symbol": ticker, "name": TICKER_NAMES.get(ticker, ticker),
        "price": round(price, 2), "change": change, "change_pct": change_pct,
        "prev_close": round(prev, 2), "volume": volume,
        "data_source": "yahoo_finance",
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/stocks", response_model=StocksResponse)
async def get_stocks(tickers: str = Query(",".join(DEFAULT_TICKERS))):
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    cache_key = "stocks:" + ",".join(sorted(ticker_list))
    cached = await cache.get(cache_key)
    if cached:
        return StocksResponse(quotes=[StockQuote(**q) for q in cached], last_updated=cached[0]["last_updated"])

    quotes = []
    for symbol in ticker_list:
        try:
            quotes.append(_fetch_yfinance(symbol))
        except Exception:
            quotes.append(generate_gbm_quote(symbol))

    await cache.set(cache_key, quotes, STOCKS_TTL)
    return StocksResponse(quotes=[StockQuote(**q) for q in quotes], last_updated=quotes[0]["last_updated"] if quotes else "")
