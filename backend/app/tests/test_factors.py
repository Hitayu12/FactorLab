import pandas as pd

from app.services.factors.lowvol import LowVolFactor
from app.services.factors.trend import TrendFactor
from app.services.factors.xsmom import XsMomFactor


def _make_monthly_px():
    idx = pd.to_datetime(
        ["2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30", "2024-05-31", "2024-06-30"]
    )
    return pd.DataFrame(
        {
            "AAA": [100, 102, 103, 104, 106, 108],
            "BBB": [100, 101, 102, 103, 104, 105],
        },
        index=idx,
    )


def test_signal_shift_no_lookahead():
    px = _make_monthly_px()
    ret = px.pct_change()

    factor = TrendFactor()
    sig_base = factor.compute_signal(px, ret, lookback_months=2)

    px_future = px.copy()
    px_future.loc["2024-04-30", "AAA"] = 1000  # extreme future move
    ret_future = px_future.pct_change()
    sig_future = factor.compute_signal(px_future, ret_future, lookback_months=2)

    # Signal at 2024-03-31 should not change based on 2024-04-30 price
    assert pd.isna(sig_base.loc["2024-03-31", "AAA"])
    assert pd.isna(sig_future.loc["2024-03-31", "AAA"])


def test_parameter_sensitivity_trend_and_xsmom():
    px = _make_monthly_px()
    ret = px.pct_change()

    trend = TrendFactor()
    sig_2 = trend.compute_signal(px, ret, lookback_months=2)
    sig_3 = trend.compute_signal(px, ret, lookback_months=3)
    assert not sig_2.equals(sig_3)

    xsmom = XsMomFactor()
    xs_2 = xsmom.compute_signal(px, ret, lookback_months=2, skip_months=1)
    xs_3 = xsmom.compute_signal(px, ret, lookback_months=3, skip_months=1)
    assert not xs_2.equals(xs_3)


def test_lowvol_prefers_lower_vol():
    idx = pd.to_datetime(["2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30"])
    ret = pd.DataFrame(
        {
            "LOW": [0.01, 0.01, 0.01, 0.01],
            "HIGH": [0.10, -0.10, 0.10, -0.10],
        },
        index=idx,
    )
    px = (1 + ret).cumprod()

    lowvol = LowVolFactor()
    sig = lowvol.compute_signal(px, ret, lookback_months=3)

    # Higher signal for lower volatility asset
    assert sig.loc["2024-04-30", "LOW"] > sig.loc["2024-04-30", "HIGH"]
