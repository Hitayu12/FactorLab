# FactorLab — Cross-Asset Factor Research and Backtesting Engine

FactorLab is a production-oriented, reproducible cross-asset factor research and backtesting platform. It is built for a **quant researcher** workflow: iterate quickly on signals, transforms, portfolio construction, and cost assumptions while maintaining strict reproducibility, bias controls, and clarity.

**Demo:** (stable URL placeholder)

## Reproducibility contract

Every run is persisted as a first-class experiment record anchored to:
- `config_json`
- `data_version_id`
- `git_commit`

Given identical `(config_json, data_version_id, git_commit)`, FactorLab must be deterministic.

## Week 1 deliverable

Week 1 provides:
- Full repo scaffolding and Docker Compose bringing up Postgres + Redis + API + Celery worker + UI.
- Working FastAPI server with `GET /health` returning FactorLab identity.
- Working Next.js frontend with routes: `/builder`, `/experiments`, `/compare`, `/experiments/[id]`.
- CI pipelines for backend and frontend.

Weeks 2–12 add DB schema, ingestion, returns, factors, backtesting, experiments, tear sheets, full UI wiring, robustness analysis, and deployment.

## Local run

```bash
cp .env.example .env
docker compose up --build
```

API:
- http://localhost:8000/health

UI:
- http://localhost:3000


## Migrations
Alembic is configured to store migration versions in `backend/app/db/migrations/`.
