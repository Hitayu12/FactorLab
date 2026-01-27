from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DataVersion(Base):
    __tablename__ = "data_versions"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    source: Mapped[str] = mapped_column(sa.String(64), nullable=False)
    created_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime, server_default=sa.func.now(), nullable=False)
    meta_json: Mapped[dict] = mapped_column(sa.JSON, nullable=False, default=dict)
