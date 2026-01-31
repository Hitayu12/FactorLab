from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PriceDaily(Base):
    __tablename__ = "prices_daily"

    id: Mapped[int] = mapped_column(
        sa.Integer().with_variant(sa.BigInteger, "postgresql"),
        primary_key=True,
        autoincrement=True,
    )
    asset_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("assets.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date: Mapped[sa.Date] = mapped_column(sa.Date, index=True, nullable=False)
    adj_close: Mapped[float] = mapped_column(sa.Float, nullable=False)
    data_version_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("data_versions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    __table_args__ = (
        sa.UniqueConstraint(
            "asset_id", "date", "data_version_id", name="uq_price_asset_date_version"
        ),
    )
