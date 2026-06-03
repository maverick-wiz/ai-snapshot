"""
GET/PUT /api/users/{id}/preferences
AISNP-28 · Owner: ATLAS
"""
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import User, UserPreference
from app.schemas import PreferenceUpdate
from app.routers.users import get_current_user
from app.limiter import limiter

router = APIRouter(tags=["Preferences"])

VALID_COUNTRIES = {"US","CN","DE","JP","IN","GB","FR","KR","CA","RU","IT","BR",
                   "AU","ES","MX","ID","NL","SA","TR","CH","TW","PL","SE","BE","AR"}

@router.get("/users/{user_id}/preferences")
@limiter.limit("60/minute")
async def get_preferences(request: Request, user_id: str,
                          current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    if str(current_user.id) != user_id:
        raise HTTPException(403, "Access denied")
    result = await db.execute(select(UserPreference).where(UserPreference.user_id == current_user.id))
    prefs = result.scalar_one_or_none()
    if not prefs:
        raise HTTPException(404, "Preferences not found")
    return {
        "user_id": str(current_user.id),
        "default_country": prefs.default_country,
        "watchlist_tickers": prefs.watchlist_tickers,
        "refresh_interval_secs": prefs.refresh_interval_secs,
        "news_limit": prefs.news_limit,
        "theme": prefs.theme,
    }


@router.put("/users/{user_id}/preferences")
@limiter.limit("30/minute")
async def update_preferences(request: Request, user_id: str, body: PreferenceUpdate,
                              current_user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    if str(current_user.id) != user_id:
        raise HTTPException(403, "Access denied")

    if body.default_country and body.default_country.upper() not in VALID_COUNTRIES:
        raise HTTPException(422, f"Invalid country code: {body.default_country}")
    if body.refresh_interval_secs is not None and not (2 <= body.refresh_interval_secs <= 60):
        raise HTTPException(422, "refresh_interval_secs must be between 2 and 60")
    if body.news_limit is not None and not (5 <= body.news_limit <= 100):
        raise HTTPException(422, "news_limit must be between 5 and 100")
    if body.theme and body.theme not in ("dark", "light"):
        raise HTTPException(422, "theme must be 'dark' or 'light'")

    result = await db.execute(select(UserPreference).where(UserPreference.user_id == current_user.id))
    prefs = result.scalar_one_or_none()
    if not prefs:
        raise HTTPException(404, "Preferences not found")

    if body.default_country: prefs.default_country = body.default_country.upper()
    if body.watchlist_tickers is not None: prefs.watchlist_tickers = body.watchlist_tickers
    if body.refresh_interval_secs is not None: prefs.refresh_interval_secs = body.refresh_interval_secs
    if body.news_limit is not None: prefs.news_limit = body.news_limit
    if body.theme: prefs.theme = body.theme

    await db.commit()
    return {"status": "updated", "user_id": user_id}
