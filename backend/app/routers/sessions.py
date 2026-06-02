from fastapi import APIRouter
router = APIRouter(tags=["Sessions"])
@router.get("/sessions/ping")
async def ping():
    return {"status": "Phase 2 — AISNP-29"}
