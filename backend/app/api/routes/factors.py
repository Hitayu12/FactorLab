from __future__ import annotations

from fastapi import APIRouter

from app.services.factors.registry import list_factors as list_factor_registry

router = APIRouter()


@router.get("")
def list_factors():
    return list_factor_registry()
