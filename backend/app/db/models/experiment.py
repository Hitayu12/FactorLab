from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)

    config_json: Mapped[dict] = mapped_column(sa.JSON, nullable=False)
    status: Mapped[str] = mapped_column(sa.String(16), nullable=False, index=True, default="queued")
    error_message: Mapped[str | None] = mapped_column(sa.Text, nullable=True)

    data_version_id: Mapped[int | None] = mapped_column(sa.Integer, index=True, nullable=True)
    git_commit: Mapped[str | None] = mapped_column(sa.String(64), nullable=True)

    created_at: Mapped[sa.DateTime] = mapped_column(sa.DateTime, server_default=sa.func.now(), nullable=False)
    started_at: Mapped[sa.DateTime | None] = mapped_column(sa.DateTime, nullable=True)
    completed_at: Mapped[sa.DateTime | None] = mapped_column(sa.DateTime, nullable=True)
