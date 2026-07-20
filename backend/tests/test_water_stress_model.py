"""
Tests for the Water Stress Model (WSM-1.0).
Validates deterministic behaviour, feature weighting, and scoring.
"""
from datetime import date
from app.decision_engine.water_stress_model import (
    BlockObservation,
    StressCategory,
    RecommendationType,
    calculate_stress,
    score_to_recommendation,
    generate_explanation,
    FEATURE_WEIGHTS,
    PHENOLOGY_WEIGHTS,
)


class TestFeatureWeights:
    def test_weights_sum_to_one(self):
        total = sum(FEATURE_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_phenology_weights_exist(self):
        expected_stages = ["bud_break", "flowering", "fruit_set", "veraison", "ripening", "harvest", "dormancy"]
        for stage in expected_stages:
            assert stage in PHENOLOGY_WEIGHTS


class TestStressCalculation:
    def test_critical_stress(self):
        obs = BlockObservation(
            block_id="A12",
            observation_date=date(2026, 7, 16),
            eta=2.0,
            eto=6.0,
            ndvi=0.4,
            ndvi_previous=0.7,
            soil_moisture=20.0,
            soil_moisture_seasonal_avg=50.0,
            rainfall_forecast=0.0,
            estimated_irrigation_requirement=5.0,
            phenology_stage="veraison",
        )
        result = calculate_stress(obs)
        assert result.stress_category == StressCategory.CRITICAL
        assert result.stress_score >= 81

    def test_healthy_stress(self):
        obs = BlockObservation(
            block_id="A12",
            observation_date=date(2026, 7, 16),
            eta=5.5,
            eto=6.0,
            ndvi=0.75,
            ndvi_previous=0.72,
            soil_moisture=55.0,
            soil_moisture_seasonal_avg=50.0,
            rainfall_forecast=8.0,
            estimated_irrigation_requirement=5.0,
            phenology_stage="harvest",
        )
        result = calculate_stress(obs)
        assert result.stress_category == StressCategory.HEALTHY
        assert result.stress_score <= 20

    def test_deterministic_behaviour(self):
        obs = BlockObservation(
            block_id="A12",
            observation_date=date(2026, 7, 16),
            eta=3.5,
            eto=6.0,
            ndvi=0.65,
            ndvi_previous=0.7,
            soil_moisture=40.0,
            soil_moisture_seasonal_avg=50.0,
            rainfall_forecast=0.0,
            estimated_irrigation_requirement=5.0,
            phenology_stage="flowering",
        )
        result1 = calculate_stress(obs)
        result2 = calculate_stress(obs)
        assert result1.stress_score == result2.stress_score
        assert result1.stress_category == result2.stress_category
        assert result1.confidence == result2.confidence

    def test_score_bounded_0_100(self):
        for eta, eto in [(0, 10), (10, 0), (5, 5), (0, 0)]:
            obs = BlockObservation(
                block_id="test",
                observation_date=date.today(),
                eta=eta,
                eto=eto,
                ndvi=0.5,
                ndvi_previous=0.5,
                soil_moisture=50,
                soil_moisture_seasonal_avg=50,
                rainfall_forecast=0,
                phenology_stage="harvest",
            )
            result = calculate_stress(obs)
            assert 0 <= result.stress_score <= 100

    def test_confidence_bounded_0_1(self):
        obs = BlockObservation(
            block_id="test",
            observation_date=date.today(),
            eta=3.5,
            eto=6.0,
            ndvi=0.65,
            ndvi_previous=0.7,
            soil_moisture=40,
            rainfall_forecast=0,
            phenology_stage="flowering",
        )
        result = calculate_stress(obs)
        assert 0 <= result.confidence <= 1

    def test_contributors_present(self):
        obs = BlockObservation(
            block_id="test",
            observation_date=date.today(),
            eta=3.5,
            eto=6.0,
            ndvi=0.65,
            ndvi_previous=0.7,
            soil_moisture=40,
            rainfall_forecast=0,
            phenology_stage="flowering",
        )
        result = calculate_stress(obs)
        assert len(result.contributors) == 6
        metrics = [c.metric for c in result.contributors]
        assert "water_deficit" in metrics
        assert "et_ratio" in metrics
        assert "ndvi_trend" in metrics

    def test_model_version_default(self):
        obs = BlockObservation(
            block_id="test",
            observation_date=date.today(),
            phenology_stage="harvest",
        )
        result = calculate_stress(obs)
        assert result.model_version == "WSM-1.0"

    def test_rules_triggered(self):
        obs_critical = BlockObservation(
            block_id="test",
            observation_date=date.today(),
            eta=1.0,
            eto=6.0,
            ndvi=0.3,
            ndvi_previous=0.7,
            soil_moisture=15,
            soil_moisture_seasonal_avg=50,
            rainfall_forecast=0,
            phenology_stage="veraison",
        )
        result = calculate_stress(obs_critical)
        assert "rule_critical_immediate_irrigation" in result.rules_triggered


class TestRecommendationMapping:
    def test_critical_irrigate_immediately(self):
        assert score_to_recommendation(90) == RecommendationType.IRRIGATE_IMMEDIATELY

    def test_high_irrigate_tonight(self):
        assert score_to_recommendation(70) == RecommendationType.IRRIGATE_TONIGHT

    def test_moderate_delay(self):
        assert score_to_recommendation(50) == RecommendationType.DELAY_IRRIGATION

    def test_monitor(self):
        assert score_to_recommendation(30) == RecommendationType.MONITOR

    def test_healthy_no_action(self):
        assert score_to_recommendation(10) == RecommendationType.NO_ACTION

    def test_boundary_80_irrigate_tonight(self):
        assert score_to_recommendation(80) == RecommendationType.IRRIGATE_TONIGHT

    def test_boundary_81_irrigate_immediately(self):
        assert score_to_recommendation(81) == RecommendationType.IRRIGATE_IMMEDIATELY


class TestExplanation:
    def test_explanation_contains_score(self):
        obs = BlockObservation(
            block_id="test",
            observation_date=date.today(),
            eta=3.5,
            eto=6.0,
            ndvi=0.65,
            ndvi_previous=0.7,
            soil_moisture=40,
            rainfall_forecast=0,
            phenology_stage="flowering",
        )
        result = calculate_stress(obs)
        explanation = generate_explanation(result, RecommendationType.IRRIGATE_TONIGHT)
        assert str(int(result.stress_score)) in explanation
        assert "Irrigate Tonight" in explanation
        assert "Confidence" in explanation
