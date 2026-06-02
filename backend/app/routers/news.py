"""
GET /api/news — Google News RSS per country.
AISNP-16 · Owner: OMEGA
"""
import re
import urllib.request
from datetime import datetime, timezone
from fastapi import APIRouter, Query, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
import feedparser

from app.schemas import NewsResponse, NewsArticle
from app.cache import cache, NEWS_TTL

router = APIRouter(tags=["News"])
limiter = Limiter(key_func=get_remote_address)

TOP25_COUNTRIES = {
    "US": ("en-US", "US", "en"), "CN": ("zh-CN", "CN", "zh"),
    "DE": ("de-DE", "DE", "de"), "JP": ("ja-JP", "JP", "ja"),
    "IN": ("en-IN", "IN", "en"), "GB": ("en-GB", "GB", "en"),
    "FR": ("fr-FR", "FR", "fr"), "KR": ("ko-KR", "KR", "ko"),
    "CA": ("en-CA", "CA", "en"), "RU": ("ru-RU", "RU", "ru"),
    "IT": ("it-IT", "IT", "it"), "BR": ("pt-BR", "BR", "pt"),
    "AU": ("en-AU", "AU", "en"), "ES": ("es-ES", "ES", "es"),
    "MX": ("es-MX", "MX", "es"), "ID": ("id-ID", "ID", "id"),
    "NL": ("nl-NL", "NL", "nl"), "SA": ("ar-SA", "SA", "ar"),
    "TR": ("tr-TR", "TR", "tr"), "CH": ("de-CH", "CH", "de"),
    "TW": ("zh-TW", "TW", "zh"), "PL": ("pl-PL", "PL", "pl"),
    "SE": ("sv-SE", "SE", "sv"), "BE": ("fr-BE", "BE", "fr"),
    "AR": ("es-AR", "AR", "es"),
}

NEWS_QUERY = "artificial intelligence OR semiconductor OR AI chip OR NVDA OR ASML OR machine learning"
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=400"


def _fetch_rss(hl: str, gl: str, ceid: str) -> list[dict]:
    url = f"https://news.google.com/rss/search?q={urllib.request.quote(NEWS_QUERY)}&hl={hl}&gl={gl}&ceid={ceid}"
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:100]:
            title = re.sub(r"\s*-\s*[^-]+$", "", entry.get("title", "")).strip()
            source = entry.get("source", {}).get("title", "Unknown")
            summary = re.sub(r"<[^>]+>", "", entry.get("summary", ""))[:300]
            articles.append({
                "title": title, "source": source,
                "url": entry.get("link", ""), "published_at": entry.get("published", ""),
                "summary": summary, "image_url": DEFAULT_IMAGE,
            })
        return articles
    except Exception:
        return []


@router.get("/news", response_model=NewsResponse)
async def get_news(country: str = Query("US", description="ISO-2 country code"), limit: int = Query(20, ge=1, le=100)):
    country = country.upper()
    if country not in TOP25_COUNTRIES:
        raise HTTPException(status_code=400, detail=f"Country '{country}' not in Top 25 GDP list")

    cache_key = f"news:{country}"
    cached = await cache.get(cache_key)
    if cached:
        articles = cached[:limit]
        return NewsResponse(articles=[NewsArticle(**a) for a in articles], country=country, total=len(articles), cached_at="cached")

    hl, gl, lang = TOP25_COUNTRIES[country]
    ceid = f"{gl}:{lang}"
    articles = _fetch_rss(hl, gl, ceid)

    # Fallback to en-US if too few results
    if len(articles) < 3:
        articles = _fetch_rss("en-US", "US", "US:en")

    if articles:
        await cache.set(cache_key, articles, NEWS_TTL)

    sliced = articles[:limit]
    return NewsResponse(articles=[NewsArticle(**a) for a in sliced], country=country, total=len(sliced))
