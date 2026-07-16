from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import (
    Column, String, Integer, Float, Date, DateTime, Text, JSON,
    ForeignKey, CheckConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="viewer")
    preferences = Column(JSON, default=dict)

    vineyards = relationship("Vineyard", back_populates="owner")

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'manager', 'agronomist', 'viewer')", name="valid_role"),
    )


class Vineyard(Base, TimestampMixin):
    __tablename__ = "vineyards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    boundary = Column(Text, nullable=True)  # GeoJSON
    area_hectares = Column(Float, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)

    owner = relationship("User", back_populates="vineyards")
    blocks = relationship("Block", back_populates="vineyard")


class Block(Base, TimestampMixin):
    __tablename__ = "blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    vineyard_id = Column(UUID(as_uuid=True), ForeignKey("vineyards.id"), nullable=False)
    name = Column(String(255), nullable=False)
    cultivar = Column(String(100), nullable=True)
    area_ha = Column(Float, nullable=True)
    geometry = Column(Text, nullable=True)  # GeoJSON
    planting_year = Column(String(10), nullable=True)

    vineyard = relationship("Vineyard", back_populates="blocks")
    observations = relationship("Observation", back_populates="block")
    stress_scores = relationship("StressScore", back_populates="block")
    recommendations = relationship("Recommendation", back_populates="block")

    __table_args__ = (
        Index("ix_blocks_vineyard", "vineyard_id"),
    )


class Observation(Base):
    __tablename__ = "observations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    block_id = Column(UUID(as_uuid=True), ForeignKey("blocks.id"), nullable=False)
    observation_date = Column(Date, nullable=False)
    eta = Column(Float, nullable=True)       # mm
    eto = Column(Float, nullable=True)       # mm
    kc = Column(Float, nullable=True)        # crop coefficient
    ndvi = Column(Float, nullable=True)      # 0-1
    soil_moisture = Column(Float, nullable=True)  # percentage
    temperature = Column(Float, nullable=True)     # celsius
    rainfall = Column(Float, nullable=True)        # mm
    phenology_stage = Column(String(50), nullable=True)
    data_source = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    block = relationship("Block", back_populates="observations")
    stress_score = relationship("StressScore", back_populates="observation", uselist=False)

    __table_args__ = (
        Index("ix_observations_block_date", "block_id", "observation_date", unique=True),
        Index("ix_observations_date", "observation_date"),
    )


class StressScore(Base):
    __tablename__ = "stress_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    observation_id = Column(UUID(as_uuid=True), ForeignKey("observations.id"), nullable=False)
    block_id = Column(UUID(as_uuid=True), ForeignKey("blocks.id"), nullable=False)
    stress_score = Column(Float, nullable=False)
    stress_category = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(String(20), nullable=False, default="WSM-1.0")
    contributors = Column(JSON, nullable=False, default=list)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    observation = relationship("Observation", back_populates="stress_score")
    block = relationship("Block", back_populates="stress_scores")
    recommendation = relationship("Recommendation", back_populates="stress_score", uselist=False)

    __table_args__ = (
        CheckConstraint("stress_score >= 0 AND stress_score <= 100", name="valid_stress_score"),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="valid_confidence"),
        Index("ix_stress_scores_block", "block_id"),
        Index("ix_stress_scores_generated", "generated_at"),
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    stress_score_id = Column(UUID(as_uuid=True), ForeignKey("stress_scores.id"), nullable=False)
    block_id = Column(UUID(as_uuid=True), ForeignKey("blocks.id"), nullable=False)
    recommendation_type = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    explanation = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    stress_score = relationship("StressScore", back_populates="recommendation")
    block = relationship("Block", back_populates="recommendations")
    decision_evidence = relationship("DecisionEvidence", back_populates="recommendation", uselist=False)

    __table_args__ = (
        CheckConstraint(
            "recommendation_type IN ('irrigate_immediately', 'irrigate_tonight', 'delay_irrigation', 'monitor', 'no_action')",
            name="valid_recommendation_type"
        ),
        CheckConstraint("status IN ('pending', 'accepted', 'dismissed', 'expired', 'completed')", name="valid_recommendation_status"),
        Index("ix_recommendations_block", "block_id"),
        Index("ix_recommendations_status", "status"),
    )


class DecisionEvidence(Base):
    __tablename__ = "decision_evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    recommendation_id = Column(UUID(as_uuid=True), ForeignKey("recommendations.id"), nullable=False)
    contributors_json = Column(JSON, nullable=False)
    stress_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(String(20), nullable=False, default="WSM-1.0")
    decision_rules_triggered = Column(JSON, default=list)
    explanation = Column(Text, nullable=True)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    recommendation = relationship("Recommendation", back_populates="decision_evidence")

    __table_args__ = (
        Index("ix_decision_evidence_recommendation", "recommendation_id"),
    )
