from __future__ import annotations

from datetime import datetime, timezone
from io import StringIO
from typing import Callable
from urllib.error import URLError
from urllib.request import urlopen

import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from app.db.models import Asset, DataVersion, PriceDaily

STOOQ_BASE_URL = "https://stooq.com/q/d/l/?s={symbol}&i=d"


def _stooq_symbol(ticker: str) -> str:
    return f"{ticker.lower()}.us"


def fetch_stooq_prices(ticker: str) -> pd.DataFrame | None:
    symbol = _stooq_symbol(ticker)
    url = STOOQ_BASE_URL.format(symbol=symbol)
    try:
        with urlopen(url, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
    except URLError:
        return None
    if not raw or raw.strip() == "":  # empty response
        return None
    return pd.read_csv(StringIO(raw))


def _normalize_prices(df: pd.DataFrame) -> tuple[pd.DataFrame | None, str | None]:
    if df is None or df.empty:
        return None, None

    cols = {c.lower(): c for c in df.columns}
    date_col = cols.get("date")
    close_col = cols.get("close") or cols.get("adj close") or cols.get("adj_close")
    if not date_col or not close_col:
        return None, None

    out = df[[date_col, close_col]].copy()
    out.columns = ["date", "adj_close"]
    out["date"] = pd.to_datetime(out["date"], errors="coerce").dt.date
    out["adj_close"] = pd.to_numeric(out["adj_close"], errors="coerce")
    out = out.dropna(subset=["date", "adj_close"])
    if out.empty:
        return None, close_col
    return out.sort_values("date"), close_col


def _insert_prices(
    db: Session,
    rows: list[dict],
) -> int:
    if not rows:
        return 0

    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        stmt = (
            pg_insert(PriceDaily)
            .values(rows)
            .on_conflict_do_nothing(
                index_elements=["asset_id", "date", "data_version_id"]
            )
        )
    elif dialect == "sqlite":
        stmt = (
            sqlite_insert(PriceDaily)
            .values(rows)
            .on_conflict_do_nothing(
                index_elements=["asset_id", "date", "data_version_id"]
            )
        )
    else:
        stmt = (
            pg_insert(PriceDaily)
            .values(rows)
            .on_conflict_do_nothing(
                index_elements=["asset_id", "date", "data_version_id"]
            )
        )

    result = db.execute(stmt)
    return result.rowcount or 0


def ingest_stooq_etf_prices(
    db: Session,
    assets: list[Asset],
    fetcher: Callable[[str], pd.DataFrame | None] = fetch_stooq_prices,
) -> dict:
    tickers = [asset.ticker for asset in assets]
    pulled_at = datetime.now(timezone.utc).isoformat()

    data_version = DataVersion(source="stooq", meta_json={})
    db.add(data_version)
    db.flush()

    meta: dict = {
        "source": "stooq",
        "tickers": tickers,
        "pull_timestamp": pulled_at,
        "price_field": None,
        "symbol_format": "ticker.us",
        "start_date": None,
        "end_date": None,
        "missing_tickers": [],
        "coverage": {},
    }

    total_inserted = 0
    overall_start = None
    overall_end = None

    for asset in assets:
        symbol = _stooq_symbol(asset.ticker)
        df = fetcher(asset.ticker)
        df, price_field = _normalize_prices(df)
        if meta["price_field"] is None and price_field is not None:
            meta["price_field"] = price_field
        if df is None or df.empty:
            meta["missing_tickers"].append(asset.ticker)
            meta["coverage"][asset.ticker] = {
                "symbol": symbol,
                "rows": 0,
                "start": None,
                "end": None,
                "missing": True,
            }
            continue

        start = df["date"].min()
        end = df["date"].max()
        rows = [
            {
                "asset_id": asset.id,
                "date": row.date,
                "adj_close": float(row.adj_close),
                "data_version_id": data_version.id,
            }
            for row in df.itertuples(index=False)
        ]
        inserted = _insert_prices(db, rows)
        total_inserted += inserted

        meta["coverage"][asset.ticker] = {
            "symbol": symbol,
            "rows": len(df),
            "inserted": inserted,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "missing": False,
        }

        overall_start = start if overall_start is None else min(overall_start, start)
        overall_end = end if overall_end is None else max(overall_end, end)

    meta["start_date"] = overall_start.isoformat() if overall_start else None
    meta["end_date"] = overall_end.isoformat() if overall_end else None
    data_version.meta_json = meta
    db.commit()

    return {
        "data_version_id": data_version.id,
        "inserted": total_inserted,
        "coverage": meta["coverage"],
    }
