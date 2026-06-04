"""
POST/DELETE /api/sessions — login/logout with SHA-256 session tokens.
AISNP-29 · Owner: ATLAS
"""
import uuid
import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models import User, UserSession
from app.schemas import SessionCreate, SessionResponse
from app.limiter import limiter

router = APIRouter(tags=["Sessions"])

SESSION_TTL_DAYS = 30


@router.post("/sessions", response_model=SessionResponse)
@limiter.limit("10/minute")
async def create_session(request: Request, body: SessionCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    if not user or user.username != body.username:
        raise HTTPException(401, "Invalid email or username")
    if not user.is_active:
        raise HTTPException(403, "Account is inactive")

    raw_token = secrets.token_bytes(32)
    token_hash = hashlib.sha256(raw_token).hexdigest()
    expires = datetime.utcnow() + timedelta(days=SESSION_TTL_DAYS)

    session = UserSession(
        id=uuid.uuid4(), user_id=user.id, session_token=token_hash,
        expires_at=expires, last_seen_at=datetime.utcnow(),
        user_agent=request.headers.get("user-agent")
    )
    db.add(session)
    await db.commit()

    return SessionResponse(
        session_token=token_hash,
        user_id=str(user.id),
        expires_at=expires.isoformat()
    )


@router.delete("/sessions/{token}", status_code=204)
@limiter.limit("10/minute")
async def delete_session(request: Request, token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserSession).where(UserSession.session_token == token))
    session = result.scalar_one_or_none()
    if session:
        await db.delete(session)
        await db.commit()
