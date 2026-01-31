# FactorLab — Cross-Asset Factor Research and Backtesting Engine

Methodology (v1 ETFs, Monthly Rebalance)

## 1. Universe and Data

**Universe (ETFs):** SPY, QQQ, IWM, EFA, EEM, TLT, IEF, SHY, LQD, HYG, GLD, DBC, VNQ

**Asset classes (v1):**
- Equity: SPY, QQQ, IWM, EFA, EEM
- Rates: TLT, IEF, SHY
- Credit: LQD, HYG
- Commodity: GLD, DBC
- REIT: VNQ

**Data source:** Stooq (free)

**Stored field:** daily `adj_close` in `prices_daily` (ingested from Stooq “Close”; treated as adjusted close for v1)

**Data versioning:** each ingestion creates a new `data_version_id` snapshot. Experiments reference a specific `data_version_id` so results are reproducible and auditable even as data updates over time.

## 2. Daily → Monthly Resampling

Month-end price is defined as the last available trading day in each calendar month from the daily close series (no artificial month-end interpolation). Conceptually: group by calendar month and take the last observed price (equivalent to pandas `resample("M").last()`).

## 3. Monthly Returns

**Formula:** r_t = P_t / P_{t-1} − 1

No forward fill is applied before return computation. If a ticker has no price history for a period (pre-inception) or has gaps, the return remains NaN for those dates.

## 4. Rebalancing and Timing Convention

**Rebalance frequency:** monthly.

**Lagged weights:** weights formed at month-end t are applied to returns over (t → t+1). This enforces a clean timing convention and prevents lookahead.

**Lookahead prevention:** signals use data up to t−1 if required by factor definitions; portfolio weights are based only on information available at the rebalance date.

## 5. Costs and Turnover (Placeholders)

**Turnover:** sum(abs(w_t − w_{t-1})) at rebalance dates.

**Cost model:** cost_return_t = turnover_t * (tc_bps + slippage_bps) / 10000

Costs are parameters stored in `config_json` and applied consistently in backtest calculations.

## 6. Limitations

- ETFs reduce survivorship and corporate action complexity, but do not eliminate all data issues.
- Free data can have missing days and adjustment ambiguities.
- v1 does not include point-in-time fundamentals.
