"""
Pydantic v2 schemas — NewsArticle, StockQuote, response models.
AISNP-21 · Owner: OMEGA
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class NewsArticle(BaseModel):
    title: str
    source: str
    url: str
    published_at: str
    summary: str
    image_url: str


class NewsResponse(BaseModel):
    articles: list[NewsArticle]
    country: str
    total: int
    cached_at: Optional[str] = None


class StockQuote(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_pct: float
    prev_close: float
    volume: int
    data_source: str  # "yahoo_finance" | "gbm_fallback"
    last_updated: str


class StocksResponse(BaseModel):
    quotes: list[StockQuote]
    last_updated: str


class Country(BaseModel):
    iso2: str
    name: str
    flag: str


class UserCreate(BaseModel):
    email: str
    username: str
    display_name: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str
    username: str
    display_name: Optional[str]
    is_active: bool


class PreferenceUpdate(BaseModel):
    default_country: Optional[str] = None
    watchlist_tickers: Optional[list[str]] = None
    refresh_interval_secs: Optional[int] = None
    news_limit: Optional[int] = None
    theme: Optional[str] = None


class SessionCreate(BaseModel):
    email: str
    username: str


class SessionResponse(BaseModel):
    session_token: str
    user_id: str
    expires_at: str


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
