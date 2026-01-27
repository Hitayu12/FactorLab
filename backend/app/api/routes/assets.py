from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("")
def list_assets():
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")

@router.post("/seed")
def seed_assets():
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")
