from __future__ import annotations

import pandas as pd
from pydantic import BaseModel, Field

from app.services.factors.base import BaseFactor


class XsMomParams(BaseModel):
    lookback_months: int = Field(default=12, ge=1, description="Lookback window in months")
    skip_months: int = Field(default=1, ge=0, description="Months to skip most-recent data")


class XsMomFactor(BaseFactor):
    name = "xsmom"
    param_schema = XsMomParams

    def compute_signal(self, px_m: pd.DataFrame, ret_m: pd.DataFrame, **params) -> pd.DataFrame:
        lookback = int(params.get("lookback_months", 12))
        skip = int(params.get("skip_months", 1))

        if ret_m.empty:
            return ret_m.copy()

        ret_window = ret_m.shift(skip).rolling(window=lookback)
        trailing = ret_window.apply(lambda x: (1.0 + x).prod() - 1.0, raw=True)
        return self._lag_signal(trailing)
