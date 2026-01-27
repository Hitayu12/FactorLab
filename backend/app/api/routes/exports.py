from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import scaffold_not_implemented

router = APIRouter()

@router.get("/{experiment_id}/export/tearsheet.pdf")
def export_tearsheet(experiment_id: int):
    raise scaffold_not_implemented()
