from __future__ import annotations

import pandas as pd


def winsorize(cs: pd.DataFrame, p: float = 0.01) -> pd.DataFrame:
    if cs.empty:
        return cs.copy()
    p = max(0.0, min(0.5, float(p)))
    lower = cs.quantile(p, axis=1, interpolation="linear")
    upper = cs.quantile(1 - p, axis=1, interpolation="linear")
    clipped = cs.copy()
    clipped = clipped.where(clipped.ge(lower, axis=0), lower, axis=0)
    clipped = clipped.where(clipped.le(upper, axis=0), upper, axis=0)
    return clipped


def cross_sectional_zscore(cs: pd.DataFrame) -> pd.DataFrame:
    if cs.empty:
        return cs.copy()
    mean = cs.mean(axis=1)
    std = cs.std(axis=1, ddof=0)
    std = std.replace(0.0, pd.NA)
    return cs.sub(mean, axis=0).div(std, axis=0)
