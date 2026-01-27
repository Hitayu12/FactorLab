from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.routes import health, assets, prices, factors, experiments, exports

configure_logging()

app = FastAPI(
    title="FactorLab",
    description="Cross-Asset Factor Research and Backtesting Engine",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(health.router)
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(prices.router, prefix="/prices", tags=["prices"])
app.include_router(factors.router, prefix="/factors", tags=["factors"])
app.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
# Exports live under /experiments/{id}/export/...
app.include_router(exports.router, prefix="/experiments", tags=["exports"])
