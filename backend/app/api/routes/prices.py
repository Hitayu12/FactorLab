from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/status")
def prices_status():
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")
