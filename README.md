# FactorLab — Cross-Asset Factor Research and Backtesting Engine

FactorLab focuses on reproducible factor research: track experiments with stable inputs, enforce deterministic outputs, and generate consistent tear sheet outputs from repeatable runs. The goal is to make research results explainable, comparable, and easy to audit without hidden state.

## Reproducibility contract

Every run is persisted as a first-class experiment record anchored to:
- `config_json`
- `data_version_id`
- `git_commit`

Given identical `(config_json, data_version_id, git_commit)`, FactorLab must be deterministic.

## Week 1 Deliverable

Implemented now:
- Repo scaffolding and Docker Compose for Postgres + Redis + API + Celery worker + UI.
- FastAPI server with `GET /health` returning FactorLab identity.
- Next.js frontend routes: `/builder`, `/experiments`, `/compare`, `/experiments/[id]`.
- CI pipelines for backend and frontend.

Scaffolded (placeholders may return 501 until Week 2+):
- API route stubs for assets, prices, factors, experiments, exports.
- Data model folders and service modules for ingestion, factors, backtests, and experiments.

Weeks 2–12 add DB schema, ingestion, returns, factors, backtesting, experiments, tear sheets, full UI wiring, robustness analysis, and deployment.

## Local run

```bash
cp .env.example .env
docker compose up --build
curl http://localhost:8000/health
open http://localhost:3000
```

API:
- http://localhost:8000/health

UI:
- http://localhost:3000


## Migrations
Alembic is configured to store migration versions in `backend/app/db/migrations/`.

## Ingestion source (Week 2)
Planned source: Stooq.
