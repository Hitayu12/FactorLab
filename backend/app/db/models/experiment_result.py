from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    experiment_id: Mapped[int] = mapped_column(sa.Integer, index=True, nullable=False, unique=True)

    freq: Mapped[str] = mapped_column(sa.String(16), nullable=False, default="monthly")
    returns_json: Mapped[dict] = mapped_column(sa.JSON, nullable=False, default=dict)
    metrics_json: Mapped[dict] = mapped_column(sa.JSON, nullable=False, default=dict)
    turnover_json: Mapped[dict] = mapped_column(sa.JSON, nullable=False, default=dict)
    weights_json: Mapped[dict | None] = mapped_column(sa.JSON, nullable=True)
