from datetime import date

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models import Asset, DataVersion, PriceDaily
from app.services.backtest.returns import (
    daily_to_monthly_prices,
    get_aligned_monthly_returns,
    monthly_returns,
)


def test_monthly_prices_and_returns():
    # 3 months of daily data with month-end on Jan 31 (weekday), Feb 28 (weekday), Mar 31 (weekday)
    dates = pd.to_datetime(
        [
            "2024-01-30",
            "2024-01-31",
            "2024-02-27",
            "2024-02-28",
            "2024-03-28",
            "2024-03-29",
        ]
    )
    px_d = pd.DataFrame(
        {
            "AAA": [100, 110, 120, 121, 130, 132],
            "BBB": [200, 210, 220, 221, 230, 231],
        },
        index=dates,
    )

    px_m = daily_to_monthly_prices(px_d)
    assert list(px_m.index.strftime("%Y-%m-%d")) == ["2024-01-31", "2024-02-29", "2024-03-31"]
    assert px_m.loc["2024-01-31", "AAA"] == 110
    assert px_m.loc["2024-02-29", "AAA"] == 121
    assert px_m.loc["2024-03-31", "AAA"] == 132

    ret_m = monthly_returns(px_m)
    assert ret_m.loc["2024-02-29", "AAA"] == (121 / 110) - 1
    assert ret_m.loc["2024-03-31", "AAA"] == (132 / 121) - 1


def test_missing_data_no_forward_fill():
    dates = pd.to_datetime(["2024-01-31", "2024-02-28", "2024-03-29"])
    px_d = pd.DataFrame(
        {
            "AAA": [100, 110, 120],
            "BBB": [None, 210, 220],
        },
        index=dates,
    )
    px_m = daily_to_monthly_prices(px_d)
    ret_m = monthly_returns(px_m)

    assert pd.isna(px_m.loc["2024-01-31", "BBB"])
    assert pd.isna(ret_m.loc["2024-02-29", "BBB"])


def test_get_aligned_monthly_returns_db():
    engine = create_engine(
        "sqlite+pysqlite://",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)

    with SessionLocal() as db:
        dv = DataVersion(source="stooq", meta_json={})
        a1 = Asset(ticker="AAA", name=None, asset_class="Equity")
        a2 = Asset(ticker="BBB", name=None, asset_class="Rates")
        db.add_all([dv, a1, a2])
        db.commit()
        db.refresh(dv)
        db.refresh(a1)
        db.refresh(a2)

        rows = [
            PriceDaily(
                asset_id=a1.id, date=date(2024, 1, 31), adj_close=100, data_version_id=dv.id
            ),
            PriceDaily(
                asset_id=a1.id, date=date(2024, 2, 28), adj_close=110, data_version_id=dv.id
            ),
            PriceDaily(
                asset_id=a2.id, date=date(2024, 2, 28), adj_close=210, data_version_id=dv.id
            ),
        ]
        db.add_all(rows)
        db.commit()

        px_m, ret_m = get_aligned_monthly_returns(db, ["BBB", "AAA"], dv.id)

    assert list(px_m.columns) == ["AAA", "BBB"]
    assert list(ret_m.columns) == ["AAA", "BBB"]
    assert list(px_m.index.strftime("%Y-%m-%d")) == ["2024-01-31", "2024-02-29"]
