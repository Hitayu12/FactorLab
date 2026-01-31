from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.core.config import settings
from app.db.models import Asset

router = APIRouter()

DEFAULT_ASSET_UNIVERSE: list[tuple[str, str]] = [
    ("SPY", "Equity"),
    ("QQQ", "Equity"),
    ("IWM", "Equity"),
    ("EFA", "Equity"),
    ("EEM", "Equity"),
    ("TLT", "Rates"),
    ("IEF", "Rates"),
    ("SHY", "Rates"),
    ("LQD", "Credit"),
    ("HYG", "Credit"),
    ("GLD", "Commodity"),
    ("DBC", "Commodity"),
    ("VNQ", "REIT"),
]


@router.get("")
def list_assets(db: Session = Depends(db_session)):
    assets = db.execute(select(Asset).order_by(Asset.ticker)).scalars().all()
    return [
        {
            "id": asset.id,
            "ticker": asset.ticker,
            "name": asset.name,
            "asset_class": asset.asset_class,
        }
        for asset in assets
    ]


@router.post("/seed")
def seed_assets(db: Session = Depends(db_session)):
    if settings.ENV != "dev":
        raise HTTPException(status_code=403, detail="Assets seed is only available in dev")

    existing = set(db.execute(select(Asset.ticker)).scalars().all())
    to_insert = [
        Asset(ticker=ticker, asset_class=asset_class)
        for ticker, asset_class in DEFAULT_ASSET_UNIVERSE
        if ticker not in existing
    ]
    inserted = len(to_insert)
    if to_insert:
        db.add_all(to_insert)
        db.commit()

    total = db.execute(select(func.count()).select_from(Asset)).scalar_one()
    skipped = len(DEFAULT_ASSET_UNIVERSE) - inserted
    return {"inserted": inserted, "skipped": skipped, "total": total}
