from __future__ import annotations

import pandas as pd
from pydantic import BaseModel, Field

from app.services.factors.base import BaseFactor


class LowVolParams(BaseModel):
    lookback_months: int = Field(default=6, ge=1, description="Rolling window in months")


class LowVolFactor(BaseFactor):
    name = "lowvol"
    param_schema = LowVolParams

    def compute_signal(self, px_m: pd.DataFrame, ret_m: pd.DataFrame, **params) -> pd.DataFrame:
        lookback = int(params.get("lookback_months", 6))
        vol = ret_m.rolling(window=lookback).std()
        signal = -vol
        return self._lag_signal(signal)
