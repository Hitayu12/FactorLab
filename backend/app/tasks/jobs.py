from __future__ import annotations

from app.tasks.celery_app import celery_app

@celery_app.task(name="factorlab.noop")
def noop() -> dict:
    return {"status": "noop"}
