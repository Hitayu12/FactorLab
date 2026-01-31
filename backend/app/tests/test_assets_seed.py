from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.api.deps import db_session
from app.core.config import settings
from app.db import models  # noqa: F401
from app.db.base import Base
from app.main import app


def test_assets_seed_idempotent():
    engine = create_engine(
        "sqlite+pysqlite://",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)

    def override_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[db_session] = override_db
    original_env = settings.ENV
    settings.ENV = "dev"

    try:
        client = TestClient(app)
        first = client.post("/assets/seed")
        assert first.status_code == 200
        first_data = first.json()

        second = client.post("/assets/seed")
        assert second.status_code == 200
        second_data = second.json()

        assert second_data["inserted"] == 0
        assert second_data["total"] == first_data["total"]
    finally:
        settings.ENV = original_env
        app.dependency_overrides.clear()
