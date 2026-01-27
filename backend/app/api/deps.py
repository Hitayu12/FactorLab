from __future__ import annotations

from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_db

def db_session(db: Session = Depends(get_db)) -> Generator[Session, None, None]:
    yield db
