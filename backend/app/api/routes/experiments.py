from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("")
def list_experiments():
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")

@router.post("")
def create_experiment():
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")

@router.get("/{experiment_id}")
def get_experiment(experiment_id: int):
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")

@router.get("/{experiment_id}/results")
def get_results(experiment_id: int):
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")

@router.post("/{experiment_id}/rerun")
def rerun_experiment(experiment_id: int):
    raise HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")
