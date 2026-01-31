FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential curl libpq-dev     && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/pyproject.toml
COPY app /app/app
RUN python -m pip install --upgrade pip     && python -m pip install -e ".[dev]"

COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

EXPOSE 8000
