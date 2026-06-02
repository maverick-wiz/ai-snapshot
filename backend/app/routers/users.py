"""Stub imports for Phase 1 — full implementations in Phase 2"""
from fastapi import APIRouter

router = APIRouter(tags=["Users"])

@router.get("/users/ping")
async def ping():
    return {"status": "Phase 2 — AISNP-27"}
