"""
GET /api/db/health · GET /api/config
AISNP-30 · Owner: ATLAS
"""
import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app.db import get_db
from app.models import AppConfig

router = APIRouter(tags=["DB Health"])


@router.get("/db/health")
async def db_health(db: AsyncSession = Depends(get_db)):
    start = time.monotonic()
    try:
        await db.execute(text("SELECT 1"))
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        return {"status": "ok", "latency_ms": latency_ms}
    except Exception as e:
        return {"status": "error", "detail": str(e)}, 503


@router.get("/config")
async def get_config(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AppConfig).where(AppConfig.is_public is True))
    rows = result.scalars().all()
    return {row.config_key: row.config_value for row in rows}
