from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import scaffold_not_implemented

router = APIRouter()

@router.get("")
def list_experiments():
    raise scaffold_not_implemented()

@router.post("")
def create_experiment():
    raise scaffold_not_implemented()

@router.get("/{experiment_id}")
def get_experiment(experiment_id: int):
    raise scaffold_not_implemented()

@router.get("/{experiment_id}/results")
def get_results(experiment_id: int):
    raise scaffold_not_implemented()

@router.post("/{experiment_id}/rerun")
def rerun_experiment(experiment_id: int):
    raise scaffold_not_implemented()
