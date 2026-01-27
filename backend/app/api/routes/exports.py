from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/{experiment_id}/export/tearsheet.pdf")
def export_tearsheet(experiment_id: int):
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")
