"""create initial schema

Revision ID: 20260127_000001
Revises: 
Create Date: 2026-01-27 00:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260127_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ticker", sa.String(length=16), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("asset_class", sa.String(length=32), nullable=False),
        sa.UniqueConstraint("ticker", name="uq_assets_ticker"),
    )
    op.create_index("ix_assets_ticker", "assets", ["ticker"])

    op.create_table(
        "data_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("meta_json", sa.JSON(), nullable=False),
    )

    op.create_table(
        "experiments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("config_json", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "data_version_id",
            sa.Integer(),
            sa.ForeignKey("data_versions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("git_commit", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_experiments_status", "experiments", ["status"])
    op.create_index("ix_experiments_data_version_id", "experiments", ["data_version_id"])

    op.create_table(
        "prices_daily",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("asset_id", sa.Integer(), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("adj_close", sa.Float(), nullable=False),
        sa.Column(
            "data_version_id",
            sa.Integer(),
            sa.ForeignKey("data_versions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "asset_id", "date", "data_version_id", name="uq_price_asset_date_version"
        ),
    )
    op.create_index("ix_prices_daily_asset_id", "prices_daily", ["asset_id"])
    op.create_index("ix_prices_daily_date", "prices_daily", ["date"])
    op.create_index("ix_prices_daily_data_version_id", "prices_daily", ["data_version_id"])

    op.create_table(
        "experiment_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "experiment_id",
            sa.Integer(),
            sa.ForeignKey("experiments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("freq", sa.String(length=16), nullable=False),
        sa.Column("returns_json", sa.JSON(), nullable=False),
        sa.Column("metrics_json", sa.JSON(), nullable=False),
        sa.Column("turnover_json", sa.JSON(), nullable=False),
        sa.Column("weights_json", sa.JSON(), nullable=True),
        sa.UniqueConstraint("experiment_id", name="uq_experiment_results_experiment_id"),
    )
    op.create_index("ix_experiment_results_experiment_id", "experiment_results", ["experiment_id"])


def downgrade() -> None:
    op.drop_index("ix_experiment_results_experiment_id", table_name="experiment_results")
    op.drop_table("experiment_results")

    op.drop_index("ix_prices_daily_data_version_id", table_name="prices_daily")
    op.drop_index("ix_prices_daily_date", table_name="prices_daily")
    op.drop_index("ix_prices_daily_asset_id", table_name="prices_daily")
    op.drop_table("prices_daily")

    op.drop_index("ix_experiments_data_version_id", table_name="experiments")
    op.drop_index("ix_experiments_status", table_name="experiments")
    op.drop_table("experiments")

    op.drop_table("data_versions")

    op.drop_index("ix_assets_ticker", table_name="assets")
    op.drop_table("assets")
