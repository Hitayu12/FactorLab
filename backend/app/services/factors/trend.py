from __future__ import annotations

import pandas as pd
from pydantic import BaseModel, Field

from app.services.factors.base import BaseFactor


class TrendParams(BaseModel):
    lookback_months: int = Field(default=12, ge=1, description="Trailing return lookback in months")


class TrendFactor(BaseFactor):
    name = "trend"
    param_schema = TrendParams

    def compute_signal(self, px_m: pd.DataFrame, ret_m: pd.DataFrame, **params) -> pd.DataFrame:
        lookback = int(params.get("lookback_months", 12))
        trailing = px_m.pct_change(lookback)
        return self._lag_signal(trailing)
