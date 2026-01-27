from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import scaffold_not_implemented

router = APIRouter()

@router.get("")
def list_factors():
    raise scaffold_not_implemented()
