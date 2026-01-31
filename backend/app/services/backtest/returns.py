from __future__ import annotations

from typing import Iterable

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Asset, PriceDaily


def _normalize_tickers(tickers: Iterable[str]) -> list[str]:
    return sorted({t.strip().upper() for t in tickers if t and t.strip()})


def load_daily_prices(db: Session, tickers: Iterable[str], data_version_id: int) -> pd.DataFrame:
    tickers_list = _normalize_tickers(tickers)
    if not tickers_list:
        return pd.DataFrame()

    rows = db.execute(
        select(PriceDaily.date, Asset.ticker, PriceDaily.adj_close)
        .join(Asset, Asset.id == PriceDaily.asset_id)
        .where(Asset.ticker.in_(tickers_list))
        .where(PriceDaily.data_version_id == data_version_id)
        .order_by(PriceDaily.date, Asset.ticker)
    ).all()

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=["date", "ticker", "adj_close"])
    df["date"] = pd.to_datetime(df["date"])
    px = df.pivot(index="date", columns="ticker", values="adj_close").sort_index()
    return px.reindex(columns=tickers_list)


def daily_to_monthly_prices(px_d: pd.DataFrame) -> pd.DataFrame:
    if px_d.empty:
        return px_d.copy()
    px_d = px_d.sort_index()
    return px_d.resample("ME").last()


def monthly_returns(px_m: pd.DataFrame) -> pd.DataFrame:
    if px_m.empty:
        return px_m.copy()
    return px_m.pct_change()


def get_aligned_monthly_returns(
    db: Session,
    tickers: Iterable[str],
    data_version_id: int,
    start: str | None = None,
    end: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    px_d = load_daily_prices(db, tickers, data_version_id)
    px_m = daily_to_monthly_prices(px_d)
    ret_m = monthly_returns(px_m)

    if start:
        px_m = px_m.loc[px_m.index >= pd.to_datetime(start)]
        ret_m = ret_m.loc[ret_m.index >= pd.to_datetime(start)]
    if end:
        px_m = px_m.loc[px_m.index <= pd.to_datetime(end)]
        ret_m = ret_m.loc[ret_m.index <= pd.to_datetime(end)]

    return px_m, ret_m
