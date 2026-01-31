from __future__ import annotations

from typing import Generator

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db


def db_session(db: Session = Depends(get_db)) -> Generator[Session, None, None]:
    yield db


def scaffold_not_implemented() -> HTTPException:
    return HTTPException(status_code=501, detail="Not implemented in Week 1 scaffold")
