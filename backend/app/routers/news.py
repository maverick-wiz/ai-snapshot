"""
GET /api/news — Google News RSS per country with rate limiting.
AISNP-16 · AISNP-20 · Owner: OMEGA
"""
import re
import urllib.parse
import urllib.request
from fastapi import APIRouter, Query, HTTPException, Request
from app.schemas import NewsResponse, NewsArticle
from app.cache import cache, NEWS_TTL
from app.limiter import limiter
import feedparser

router = APIRouter(tags=["News"])

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
    url = (f"https://news.google.com/rss/search"
           f"?q={urllib.parse.quote(NEWS_QUERY)}&hl={hl}&gl={gl}&ceid={ceid}")
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:100]:
            title = re.sub(r"\s*-\s*[^-]+$", "", entry.get("title", "")).strip()
            source = entry.get("source", {}).get("title", "Unknown")
            summary = re.sub(r"<[^>]+>", "", entry.get("summary", ""))[:300]
            articles.append({
                "title": title, "source": source,
                "url": entry.get("link", ""),
                "published_at": entry.get("published", ""),
                "summary": summary, "image_url": DEFAULT_IMAGE,
            })
        return articles
    except Exception:
        return []


@router.get("/news", response_model=NewsResponse)
@limiter.limit("30/minute")
async def get_news(
    request: Request,
    country: str = Query("US", description="ISO-2 country code"),
    limit: int = Query(20, ge=1, le=100),
):
    country = country.upper()
    if country not in TOP25_COUNTRIES:
        raise HTTPException(400, detail=f"Country '{country}' not in Top 25 GDP list")

    cache_key = f"news:{country}"
    cached = await cache.get(cache_key)
    if cached:
        return NewsResponse(
            articles=[NewsArticle(**a) for a in cached[:limit]],
            country=country, total=len(cached[:limit]), cached_at="cached"
        )

    hl, gl, lang = TOP25_COUNTRIES[country]
    articles = _fetch_rss(hl, gl, f"{gl}:{lang}")
    if len(articles) < 3:
        articles = _fetch_rss("en-US", "US", "US:en")

    if articles:
        await cache.set(cache_key, articles, NEWS_TTL)

    sliced = articles[:limit]
    return NewsResponse(articles=[NewsArticle(**a) for a in sliced],
                        country=country, total=len(sliced))
