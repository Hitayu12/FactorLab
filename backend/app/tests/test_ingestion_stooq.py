from datetime import date

import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models import Asset, DataVersion, PriceDaily
from app.services.ingestion.etf_ingest import ingest_stooq_etf_prices


def test_stooq_ingestion_creates_version_and_prices():
    engine = create_engine(
        "sqlite+pysqlite://",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)

    def fake_fetcher(_: str) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Date": [date(2024, 1, 1), date(2024, 1, 1), date(2024, 1, 2)],
                "Close": [100.0, 100.0, 101.5],
            }
        )

    with SessionLocal() as db:
        asset = Asset(ticker="SPY", name=None, asset_class="Equity")
        db.add(asset)
        db.commit()
        db.refresh(asset)

        result = ingest_stooq_etf_prices(db, [asset], fetcher=fake_fetcher)

        data_versions = db.execute(select(DataVersion)).scalars().all()
        assert len(data_versions) == 1
        data_version = data_versions[0]
        assert result["data_version_id"] == data_version.id
        assert data_version.meta_json["price_field"] == "Close"
        assert data_version.meta_json["symbol_format"] == "ticker.us"
        assert "SPY" in data_version.meta_json["coverage"]
        assert data_version.meta_json["coverage"]["SPY"]["symbol"] == "spy.us"

        prices = db.execute(select(PriceDaily)).scalars().all()
        assert len(prices) == 2  # duplicate date ignored
        assert all(p.data_version_id == data_version.id for p in prices)
