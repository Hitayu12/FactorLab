from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(sa.String(16), unique=True, index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(sa.String(128), nullable=True)
    asset_class: Mapped[str] = mapped_column(sa.String(32), nullable=False)
