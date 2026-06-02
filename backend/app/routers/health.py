"""Health check endpoint. AISNP-15 · Owner: OMEGA"""
import time
from fastapi import APIRouter
from app.schemas import HealthResponse

router = APIRouter(tags=["Health"])
_start_time = time.time()

@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", version="1.0.0", uptime_seconds=round(time.time() - _start_time, 1))
