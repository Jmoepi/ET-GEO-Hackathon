"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-07-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "users",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="viewer"),
        sa.Column("preferences", sa.JSON, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "vineyards",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("owner_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("location_lat", sa.Float, nullable=True),
        sa.Column("location_lon", sa.Float, nullable=True),
        sa.Column("boundary", sa.Text, nullable=True),
        sa.Column("area_hectares", sa.Float, nullable=True),
        sa.Column("metadata", sa.JSON, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "blocks",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vineyard_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("vineyards.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("cultivar", sa.String(100), nullable=True),
        sa.Column("area_ha", sa.Float, nullable=True),
        sa.Column("geometry", sa.Text, nullable=True),
        sa.Column("planting_year", sa.String(10), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_blocks_vineyard", "blocks", ["vineyard_id"])

    op.create_table(
        "observations",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("block_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("blocks.id"), nullable=False),
        sa.Column("observation_date", sa.Date, nullable=False),
        sa.Column("eta", sa.Float, nullable=True),
        sa.Column("eto", sa.Float, nullable=True),
        sa.Column("kc", sa.Float, nullable=True),
        sa.Column("ndvi", sa.Float, nullable=True),
        sa.Column("soil_moisture", sa.Float, nullable=True),
        sa.Column("temperature", sa.Float, nullable=True),
        sa.Column("rainfall", sa.Float, nullable=True),
        sa.Column("phenology_stage", sa.String(50), nullable=True),
        sa.Column("data_source", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_observations_block_date", "observations", ["block_id", "observation_date"], unique=True)
    op.create_index("ix_observations_date", "observations", ["observation_date"])

    op.create_table(
        "stress_scores",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("observation_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("observations.id"), nullable=False),
        sa.Column("block_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("blocks.id"), nullable=False),
        sa.Column("stress_score", sa.Float, nullable=False),
        sa.Column("stress_category", sa.String(20), nullable=False),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("model_version", sa.String(20), nullable=False, server_default="WSM-1.0"),
        sa.Column("contributors", sa.JSON, nullable=False, server_default="[]"),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("stress_score >= 0 AND stress_score <= 100", name="valid_stress_score"),
        sa.CheckConstraint("confidence >= 0 AND confidence <= 1", name="valid_confidence"),
    )
    op.create_index("ix_stress_scores_block", "stress_scores", ["block_id"])
    op.create_index("ix_stress_scores_generated", "stress_scores", ["generated_at"])

    op.create_table(
        "recommendations",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("stress_score_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("stress_scores.id"), nullable=False),
        sa.Column("block_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("blocks.id"), nullable=False),
        sa.Column("recommendation_type", sa.String(50), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("explanation", sa.Text, nullable=True),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint(
            "recommendation_type IN ('irrigate_immediately', 'irrigate_tonight', 'delay_irrigation', 'monitor', 'no_action')",
            name="valid_recommendation_type",
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'accepted', 'dismissed', 'expired', 'completed')",
            name="valid_recommendation_status",
        ),
    )
    op.create_index("ix_recommendations_block", "recommendations", ["block_id"])
    op.create_index("ix_recommendations_status", "recommendations", ["status"])

    op.create_table(
        "decision_evidence",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("recommendation_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("recommendations.id"), nullable=False),
        sa.Column("contributors_json", sa.JSON, nullable=False),
        sa.Column("stress_score", sa.Float, nullable=False),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("model_version", sa.String(20), nullable=False, server_default="WSM-1.0"),
        sa.Column("decision_rules_triggered", sa.JSON, server_default="[]"),
        sa.Column("explanation", sa.Text, nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_decision_evidence_recommendation", "decision_evidence", ["recommendation_id"])


def downgrade() -> None:
    op.drop_table("decision_evidence")
    op.drop_table("recommendations")
    op.drop_table("stress_scores")
    op.drop_table("observations")
    op.drop_table("blocks")
    op.drop_table("vineyards")
    op.drop_table("users")
