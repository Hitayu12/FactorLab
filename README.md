# FactorLab — Cross-Asset Factor Research Engine

A reproducible, bias-aware research & backtesting platform for systematic factor strategies across a core cross-asset ETF universe.
---

## Project Summary

**FactorLab** is a cross-asset factor research platform designed to emulate how systematic teams run research in practice: **versioned data**, **deterministic pipelines**, **explicit timing rules to prevent lookahead**, and **testable factor + backtest components**.

The platform is built around a simple principle: every result should be reproducible from (a) the **data version**, (b) the **exact configuration**, and (c) the **code state** that produced it. This repo currently supports a **Stooq-ingested ETF universe**, **monthly resampling + returns**, and a **factor framework** (Trend, XsMom, LowVol) with transforms and lookahead guards.

---

## Current State

Right now I’ve got the core research plumbing in place: versioned data ingestion, monthly return construction, and a working factor framework (Trend/XsMom/LowVol) with lookahead guards and a test suite. The APIs for seeding assets, ingesting prices, and listing factors are live, and everything runs cleanly in Docker with CI checks. Next is converting signals into portfolio weights (constraints + turnover), then building a lagged-weight backtest engine with transaction costs, and finally adding experiments + UI so it’s usable end-to-end.

---

## Tech Stack

* Backend: Python (FastAPI-style service layout), SQLAlchemy 2.0, Alembic
* Data: Postgres schema for assets, prices, data versions, experiments, results
* Async (planned Week 7): Celery worker with Redis broker
* Frontend (planned Week 9+): Next.js UI (“Builder” + “Results Explorer”)
* Tooling: Docker Compose, GitHub Actions, Ruff, Pytest

---

## Quickstart

> Assumes you’re running from the repo root.

### 1) Start services (Docker Compose)

```bash
docker compose up --build
```

Healthchecks are configured for backend and frontend; worker depends on healthy Postgres/Redis and a started backend container.

### 2) Run backend tests

```bash
docker compose exec backend pytest -q app/tests
```

### 3) Lint / format checks

```bash
docker compose exec backend ruff check app
docker compose exec backend ruff format --check app
```

---

## API Overview

### Assets

* `GET /assets`

  * Returns all assets ordered by ticker.
* `POST /assets/seed` *(dev-only)*

  * Seeds the default ETF universe:
    `SPY, QQQ, IWM, EFA, EEM, TLT, IEF, SHY, LQD, HYG, GLD, DBC, VNQ`
  * Idempotent; returns inserted/skipped/total.

### Prices / Ingestion

* `POST /prices/ingest` *(dev-only)*

  * Runs synchronous Stooq ingestion for all seeded assets.
  * Returns `data_version_id`, inserted counts, and coverage summary.
* `GET /prices/status`

  * Coverage for latest `data_version_id` (max id): per ticker `min_date`, `max_date`, `count_days`.
  * 404 if no `data_versions` exist.

### Factors

* `GET /factors`

  * Returns the factor registry: names, parameter schema, defaults.

---

## Data & Methodology

### Data ingestion + versioning

* Each ingestion run creates a new row in `data_versions` with `source="stooq"`.
* Adjusted closes are written to `prices_daily` with `ON CONFLICT DO NOTHING`.
* Missing data/tickers are handled gracefully and recorded in `meta_json` (coverage, timestamps, symbol format, etc.).

### Daily → monthly resampling

* Month-end prices use the **last trading day** of each month.
* Monthly returns are computed as `pct_change()` from month-end prices.
* No forward-fill is applied prior to return computation; NaNs persist for pre-inception/missing data.

### Lookahead prevention (research correctness)

* Factor signals are computed on monthly inputs and **delayed** to prevent lookahead.
* Lookahead audits verify that a “future spike” does not change earlier signals for implemented factors; XsMom may produce NaNs early when lookback/skip requirements aren’t met (expected behavior).


## Weekly Progress (Week 0 → Week 12)

### Week 0 — Repo & Dev Environment *(Completed)*

* Docker Compose configured for backend + worker + services with healthchecks.
* Backend image uses editable install for reliable imports in-container.
* CI runs `pip install -e "./backend[dev]"` and executes tests from `backend/app/tests`.

### Week 1 — Packaging & Import Stability *(Completed)*

* Added missing `__init__.py` files across backend to stabilize runtime imports and pytest collection.
* Standardized model exports via `backend/app/db/models/__init__.py` with `__all__`.

### Week 2 — Database Schema + Ingestion API *(Completed)*

* Implemented SQLAlchemy 2.0 models for:

  * `assets`, `data_versions`, `prices_daily`, `experiments`, `experiment_results`
* Alembic configured to load models and manage migrations; initial schema migration created.
* API endpoints added:

  * asset list/seed
  * ingestion trigger
  * ingestion coverage/status
* Stooq ingestion service:

  * creates `data_versions` record
  * ingests adjusted close series into `prices_daily`
  * records coverage + missing data into `meta_json`

### Week 3 — Monthly Returns + Research Documentation *(Completed)*

* Implemented daily price loader, month-end resampling, monthly return computation, and aligned return retrieval.
* Added `research/methodology.md` documenting:

  * universe + data source
  * data_version reproducibility
  * resampling and annualization conventions
  * timing rules / lookahead prevention
  * known limitations and placeholders (turnover/cost models).

### Week 4 — Factor Framework + Tests *(Completed)*

* Built factor interface + registry and exposed registry via `/factors`.
* Implemented: Trend, XsMom, LowVol (monthly inputs, delayed signals).
* Added transforms: winsorize and cross-sectional z-score (`ddof=0`).
* Expanded test coverage + QA checks (pytest + ruff + lookahead audits).

### Week 5 — Portfolio Construction + Constraints + Turnover *(Planned)*

**Goal:** Convert signals → portfolio weights deterministically.

* Implement `long_only` and `long_short` constructors (top-k / bottom-k selection, equal & signal-weighting).
* Enforce constraints (`max_weight`, `gross_leverage`) and compute turnover at rebalance dates.
* Add must-have tests: weight sums, gross/net exposure, max weight enforcement, deterministic tie-breaking, turnover sanity.

### Week 6 — Backtest Engine + Lagged Weights + Transaction Costs *(Planned)*

**Goal:** Compute returns with strict timing (anti-lookahead hardening).

* Backtest engine where weights formed at month-end `t` apply to returns `t → t+1`.
* Cost model using turnover with `tc_bps` + `slippage_bps`; verify monotonic cost impact.
* Add lookahead test: “future spike doesn’t change earlier result.”

### Week 7 — Experiments + Async Pipeline + Persistence *(Planned)*

**Goal:** Reproducible experiment orchestration (submit → queued → running → results).

* POST `/experiments` validates config, locks latest `data_version_id`, stores `git_commit`, queues Celery job.
* Worker runs full pipeline and persists results; robust failure reporting (`error_message`).
* GET endpoints for experiment status + results; rerun clones config into a new record.

### Week 8 — Analytics Metrics + PDF Tear Sheet Export *(Planned)*

**Goal:** Interpretable results + exportable artifact.

* Implement metrics (CAGR, vol, Sharpe/Sortino, max drawdown, Calmar, hit rate, turnover stats).
* Add tear sheet PDF export: equity curve, drawdowns, rolling Sharpe; clean 1–3 page layout.
* Store metrics in `metrics_json` and expose export endpoint.

### Week 9 — Frontend Wiring: Builder + Results Explorer *(Planned)*

**Goal:** First “mini research terminal” UX.

* Builder UI pulls `/factors`, generates dynamic param forms, submits `/experiments`, polls status.
* Results page renders metrics + charts + PDF download link.
* Keep backtest logic server-side only.

### Week 10 — Experiment Library + Compare View *(Planned)*

**Goal:** Multi-run workflow: list → inspect → compare.

* Table view of experiments with sortable metric columns (from `metrics_json`).
* Compare view: overlay equity curves, metrics side-by-side, returns correlation matrix with aligned dates.

### Week 11 — Robustness & Scientific Rigor *(Planned)*

**Goal:** Demonstrate research hygiene and overfitting awareness.

* Parameter sweeps (e.g., trend lookbacks), stored as normal experiments.
* Out-of-sample splits and regime slicing (document regime definition if proxy-based).
* Summarize tradeoffs (Sharpe vs turnover vs drawdown) and limitations.

### Week 12 — Deployment + Final Docs + Demo Assets *(Planned)*

**Goal:** Recruiter-ready demo with stable artifacts.

* Deploy backend + worker + DB + broker; deploy frontend pointing to backend.
* README updated with demo link + screenshots and a short demo script.
* Produce `research/report.pdf` (results + sensitivity + OOS + regimes + limitations).
* Ensure local reproducibility via Docker Compose and no missing env vars in demo.
  (Deployment provider TBD: e.g., Vercel, Render, Fly.io, or Railway.)

---
