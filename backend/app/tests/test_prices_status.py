from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.api.deps import db_session
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models import Asset, DataVersion, PriceDaily
from app.main import app


def test_prices_status_latest_coverage():
    engine = create_engine(
        "sqlite+pysqlite://",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)

    def override_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[db_session] = override_db
    try:
        with TestingSessionLocal() as db:
            asset_a = Asset(ticker="SPY", name=None, asset_class="Equity")
            asset_b = Asset(ticker="TLT", name=None, asset_class="Rates")
            db.add_all([asset_a, asset_b])
            db.commit()
            db.refresh(asset_a)
            db.refresh(asset_b)

            dv1 = DataVersion(source="stooq", meta_json={})
            dv2 = DataVersion(source="stooq", meta_json={})
            db.add_all([dv1, dv2])
            db.commit()
            db.refresh(dv1)
            db.refresh(dv2)
            dv2_id = dv2.id

            prices = [
                PriceDaily(
                    asset_id=asset_a.id,
                    date=date(2024, 1, 1),
                    adj_close=100.0,
                    data_version_id=dv2.id,
                ),
                PriceDaily(
                    asset_id=asset_a.id,
                    date=date(2024, 1, 2),
                    adj_close=101.0,
                    data_version_id=dv2.id,
                ),
                PriceDaily(
                    asset_id=asset_b.id,
                    date=date(2024, 1, 1),
                    adj_close=90.0,
                    data_version_id=dv2.id,
                ),
            ]
            db.add_all(prices)
            db.commit()

        client = TestClient(app)
        resp = client.get("/prices/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["data_version_id"] == dv2_id
        assert data["source"] == "stooq"
        assert len(data["coverage"]) == 2

        spy = next(row for row in data["coverage"] if row["ticker"] == "SPY")
        assert spy["asset_class"] == "Equity"
        assert spy["min_date"] == "2024-01-01"
        assert spy["max_date"] == "2024-01-02"
        assert spy["count_days"] == 2
    finally:
        app.dependency_overrides.clear()
