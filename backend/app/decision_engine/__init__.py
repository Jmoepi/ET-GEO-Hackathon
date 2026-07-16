"""
Decision Intelligence Engine
Assembles context, calculates stress, generates recommendations with DEP.
"""
from uuid import UUID, uuid4
from datetime import date, datetime, timezone
from dataclasses import dataclass, asdict
from typing import Optional
from app.decision_engine.water_stress_model import (
    BlockObservation,
    StressResult,
    calculate_stress,
    score_to_recommendation,
    generate_explanation,
    StressCategory,
    RecommendationType,
)


@dataclass
class DecisionEvidencePackage:
    decision_id: str
    block_id: str
    observation_date: date
    stress_score: float
    stress_category: str
    confidence: float
    model_version: str
    contributors: list[dict]
    decision_rules_triggered: list[str]
    recommendation: str
    explanation: str
    generated_at: str


def generate_decision(observation: BlockObservation) -> tuple[StressResult, RecommendationType, DecisionEvidencePackage]:
    stress_result = calculate_stress(observation)
    recommendation = score_to_recommendation(stress_result.stress_score)
    explanation = generate_explanation(stress_result, recommendation)

    dep = DecisionEvidencePackage(
        decision_id=f"DEP-{observation.observation_date.strftime('%Y%m%d')}-{observation.block_id}",
        block_id=observation.block_id,
        observation_date=observation.observation_date,
        stress_score=stress_result.stress_score,
        stress_category=stress_result.stress_category.value,
        confidence=stress_result.confidence,
        model_version=stress_result.model_version,
        contributors=[asdict(c) for c in stress_result.contributors],
        decision_rules_triggered=stress_result.rules_triggered,
        recommendation=recommendation.value,
        explanation=explanation,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    return stress_result, recommendation, dep
