"""
Users CRUD — POST /api/users · GET /api/users/{id}
AISNP-27 · Owner: ATLAS
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.db import get_db
from app.models import User, UserPreference, UserSession
from app.schemas import UserCreate, UserResponse
from app.limiter import limiter
from fastapi import Request

router = APIRouter(tags=["Users"])

VALID_COUNTRIES = {"US","CN","DE","JP","IN","GB","FR","KR","CA","RU","IT","BR",
                   "AU","ES","MX","ID","NL","SA","TR","CH","TW","PL","SE","BE","AR"}


async def get_current_user(
    x_session_token: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not x_session_token:
        raise HTTPException(401, "X-Session-Token header required")
    result = await db.execute(
        select(UserSession).where(
            UserSession.session_token == x_session_token,
            UserSession.expires_at > datetime.utcnow()
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(401, "Invalid or expired session token")
    session.last_seen_at = datetime.utcnow()
    result2 = await db.execute(select(User).where(User.id == session.user_id))
    user = result2.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    await db.commit()
    return user


@router.post("/users", response_model=UserResponse, status_code=201)
@limiter.limit("10/minute")
async def create_user(request: Request, body: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check duplicates
    existing = await db.execute(
        select(User).where((User.email == body.email) | (User.username == body.username))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Email or username already exists")

    user = User(id=uuid.uuid4(), email=body.email, username=body.username,
                display_name=body.display_name)
    db.add(user)
    await db.flush()

    prefs = UserPreference(
        id=uuid.uuid4(), user_id=user.id, default_country="US",
        watchlist_tickers=["NVDA","AMD","TSM","ASML","MSFT","AVGO"],
        refresh_interval_secs=5, news_limit=20, theme="dark"
    )
    db.add(prefs)
    await db.commit()
    await db.refresh(user)
    return UserResponse(id=str(user.id), email=user.email, username=user.username,
                        display_name=user.display_name, is_active=user.is_active)


@router.get("/users/{user_id}", response_model=UserResponse)
@limiter.limit("60/minute")
async def get_user(request: Request, user_id: str,
                   current_user: User = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(403, "Access denied")
    return UserResponse(id=str(current_user.id), email=current_user.email,
                        username=current_user.username,
                        display_name=current_user.display_name,
                        is_active=current_user.is_active)
