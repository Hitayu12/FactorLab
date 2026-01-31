from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.core.config import settings
from app.db.models import Asset, DataVersion, PriceDaily
from app.services.ingestion.etf_ingest import ingest_stooq_etf_prices

router = APIRouter()


@router.get("/status")
def prices_status(db: Session = Depends(db_session)):
    latest_id = db.execute(
        select(DataVersion.id).order_by(DataVersion.id.desc()).limit(1)
    ).scalar_one_or_none()
    if latest_id is None:
        raise HTTPException(status_code=404, detail="No data ingested yet")

    data_version = db.get(DataVersion, latest_id)
    coverage_rows = db.execute(
        select(
            Asset.ticker,
            Asset.asset_class,
            func.min(PriceDaily.date).label("min_date"),
            func.max(PriceDaily.date).label("max_date"),
            func.count().label("count_days"),
        )
        .join(PriceDaily, PriceDaily.asset_id == Asset.id)
        .where(PriceDaily.data_version_id == latest_id)
        .group_by(Asset.ticker, Asset.asset_class)
        .order_by(Asset.ticker)
    ).all()

    coverage = [
        {
            "ticker": row.ticker,
            "asset_class": row.asset_class,
            "min_date": row.min_date.isoformat() if row.min_date else None,
            "max_date": row.max_date.isoformat() if row.max_date else None,
            "count_days": row.count_days,
        }
        for row in coverage_rows
    ]

    return {
        "data_version_id": latest_id,
        "source": data_version.source if data_version else None,
        "coverage": coverage,
    }


@router.post("/ingest")
def ingest_prices(db: Session = Depends(db_session)):
    if settings.ENV != "dev":
        raise HTTPException(status_code=403, detail="Prices ingest is only available in dev")

    assets = db.execute(select(Asset).order_by(Asset.ticker)).scalars().all()
    if not assets:
        raise HTTPException(status_code=400, detail="No assets found; seed /assets/seed first")

    return ingest_stooq_etf_prices(db, assets)
