"""
Geometric Brownian Motion fallback for when yfinance is unavailable.
AISNP-39 · Owner: OMEGA
"""
import math
import random
import time
from datetime import datetime, timezone

# Baseline prices (approximate real-world anchors)
GBM_BASELINES = {
    "NVDA": {"price": 880.0, "name": "NVIDIA Corporation"},
    "AMD":  {"price": 165.0, "name": "Advanced Micro Devices"},
    "TSM":  {"price": 190.0, "name": "Taiwan Semiconductor Mfg"},
    "ASML": {"price": 720.0, "name": "ASML Holding N.V."},
    "MSFT": {"price": 425.0, "name": "Microsoft Corporation"},
    "AVGO": {"price": 1690.0, "name": "Broadcom Inc."},
}

# GBM state: tracks current simulated price per symbol
_gbm_state: dict[str, float] = {}

MU = 0.0002      # drift
SIGMA = 0.018    # volatility
DT = 1 / 252     # one trading day


def _next_gbm_price(symbol: str) -> float:
    baseline = GBM_BASELINES.get(symbol, {}).get("price", 100.0)
    current = _gbm_state.get(symbol, baseline)
    z = random.gauss(0, 1)
    next_price = current * math.exp((MU - 0.5 * SIGMA ** 2) * DT + SIGMA * math.sqrt(DT) * z)
    _gbm_state[symbol] = next_price
    return round(next_price, 2)


def generate_gbm_quote(symbol: str) -> dict:
    info = GBM_BASELINES.get(symbol, {"price": 100.0, "name": symbol})
    price = _next_gbm_price(symbol)
    prev_close = round(price * (1 + random.uniform(-0.02, 0.02)), 2)
    change = round(price - prev_close, 2)
    change_pct = round((change / prev_close) * 100, 2) if prev_close else 0.0
    baseline_vol = int(info["price"] * 1_000_000 / 100)
    volume = int(baseline_vol * random.uniform(0.8, 1.2))
    return {
        "symbol": symbol,
        "name": info["name"],
        "price": price,
        "change": change,
        "change_pct": change_pct,
        "prev_close": prev_close,
        "volume": volume,
        "data_source": "gbm_fallback",
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }
