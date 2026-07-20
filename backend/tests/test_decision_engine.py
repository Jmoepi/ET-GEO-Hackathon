"""
Tests for the Decision Intelligence Engine.
"""
from datetime import date
from app.decision_engine import generate_decision
from app.decision_engine.water_stress_model import BlockObservation, RecommendationType


class TestDecisionGeneration:
    def test_generates_complete_dep(self):
        obs = BlockObservation(
            block_id="A12",
            observation_date=date(2026, 7, 16),
            eta=3.5,
            eto=6.0,
            ndvi=0.65,
            ndvi_previous=0.7,
            soil_moisture=40,
            soil_moisture_seasonal_avg=50,
            rainfall_forecast=0,
            estimated_irrigation_requirement=5,
            phenology_stage="veraison",
        )
        stress, recommendation, dep = generate_decision(obs)

        assert dep.block_id == "A12"
        assert dep.model_version == "WSM-1.0"
        assert dep.stress_category in ["healthy", "monitor", "moderate", "high", "critical"]
        assert 0 <= dep.stress_score <= 100
        assert 0 <= dep.confidence <= 1
        assert len(dep.contributors) == 6
        assert isinstance(dep.decision_rules_triggered, list)
        assert dep.explanation
        assert dep.recommendation in [r.value for r in RecommendationType]

    def test_recommendation_matches_stress(self):
        obs_critical = BlockObservation(
            block_id="A12",
            observation_date=date(2026, 7, 16),
            eta=1.0,
            eto=6.0,
            ndvi=0.3,
            ndvi_previous=0.7,
            soil_moisture=15,
            soil_moisture_seasonal_avg=50,
            rainfall_forecast=0,
            phenology_stage="veraison",
        )
        _, recommendation, _ = generate_decision(obs_critical)
        assert recommendation == RecommendationType.IRRIGATE_IMMEDIATELY

    def test_dep_decision_id_format(self):
        obs = BlockObservation(
            block_id="B05",
            observation_date=date(2026, 7, 16),
            eta=3.5,
            eto=6.0,
            phenology_stage="flowering",
        )
        _, _, dep = generate_decision(obs)
        assert dep.decision_id.startswith("DEP-20260716-B05")
