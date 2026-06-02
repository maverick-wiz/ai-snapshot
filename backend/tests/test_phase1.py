"""
Basic backend tests — Phase 1 scaffold.
AISNP-23 · Owner: OMEGA + DELTA
Full test suite to be expanded in Phase 2 (AISNP-23, AISNP-44, AISNP-46).
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert "uptime_seconds" in data


def test_countries_returns_25():
    r = client.get("/api/countries")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 25
    codes = [c["iso2"] for c in data]
    assert "US" in codes
    assert "DE" in codes
    assert "JP" in codes


def test_news_invalid_country():
    r = client.get("/api/news?country=ZZ")
    assert r.status_code == 400


def test_news_valid_country_schema():
    with patch("app.routers.news._fetch_rss") as mock_rss:
        mock_rss.return_value = [{
            "title": "AI breakthrough",
            "source": "TechCrunch",
            "url": "https://example.com",
            "published_at": "2026-06-01T10:00:00",
            "summary": "An amazing AI development",
            "image_url": "https://example.com/img.jpg"
        }]
        r = client.get("/api/news?country=US&limit=1")
    assert r.status_code == 200
    data = r.json()
    assert "articles" in data
    assert data["country"] == "US"


def test_stocks_gbm_fallback():
    """When yfinance fails, GBM fallback activates and data_source = gbm_fallback."""
    with patch("app.routers.stocks._fetch_yfinance", side_effect=Exception("yfinance down")):
        r = client.get("/api/stocks?tickers=NVDA")
    assert r.status_code == 200
    data = r.json()
    assert len(data["quotes"]) == 1
    assert data["quotes"][0]["data_source"] == "gbm_fallback"
    assert data["quotes"][0]["symbol"] == "NVDA"


def test_stocks_schema_fields():
    """All required StockQuote fields present."""
    with patch("app.routers.stocks._fetch_yfinance") as mock_yf:
        mock_yf.return_value = {
            "symbol": "NVDA", "name": "NVIDIA Corporation",
            "price": 880.0, "change": 5.0, "change_pct": 0.57,
            "prev_close": 875.0, "volume": 50000000,
            "data_source": "yahoo_finance", "last_updated": "2026-06-01T10:00:00Z"
        }
        r = client.get("/api/stocks?tickers=NVDA")
    assert r.status_code == 200
    q = r.json()["quotes"][0]
    for field in ["symbol", "name", "price", "change", "change_pct", "prev_close", "volume", "data_source", "last_updated"]:
        assert field in q, f"Missing field: {field}"


def test_gbm_generates_prices():
    from app.gbm import generate_gbm_quote
    quote = generate_gbm_quote("NVDA")
    assert quote["symbol"] == "NVDA"
    assert quote["data_source"] == "gbm_fallback"
    assert 400 < quote["price"] < 2000  # within 50% of ~880 baseline
    assert "last_updated" in quote


def test_config_endpoint():
    r = client.get("/api/config")
    assert r.status_code == 200
    data = r.json()
    assert "default_tickers" in data
    assert "NVDA" in data["default_tickers"]
