"""
Water Stress Model (WSM-1.0)
Deterministic weighted linear model for vineyard irrigation urgency scoring.

Implements the specification from docs/07-Water-Stress-Model.md
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from enum import Enum


class StressCategory(str, Enum):
    HEALTHY = "healthy"
    MONITOR = "monitor"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationType(str, Enum):
    IRRIGATE_IMMEDIATELY = "irrigate_immediately"
    IRRIGATE_TONIGHT = "irrigate_tonight"
    DELAY_IRRIGATION = "delay_irrigation"
    MONITOR = "monitor"
    NO_ACTION = "no_action"


PHENOLOGY_WEIGHTS = {
    "bud_break": 0.50,
    "flowering": 0.80,
    "fruit_set": 0.80,
    "veraison": 1.00,
    "ripening": 0.85,
    "harvest": 0.30,
    "dormancy": 0.10,
}

FEATURE_WEIGHTS = {
    "water_deficit": 0.30,
    "et_ratio": 0.20,
    "soil_moisture": 0.20,
    "ndvi_trend": 0.15,
    "rainfall_offset": 0.10,
    "phenology": 0.05,
}

STRESS_THRESHOLDS = {
    StressCategory.HEALTHY: (0, 20),
    StressCategory.MONITOR: (21, 40),
    StressCategory.MODERATE: (41, 60),
    StressCategory.HIGH: (61, 80),
    StressCategory.CRITICAL: (81, 100),
}

RECOMMENDATION_THRESHOLDS = [
    (81, RecommendationType.IRRIGATE_IMMEDIATELY),
    (61, RecommendationType.IRRIGATE_TONIGHT),
    (41, RecommendationType.DELAY_IRRIGATION),
    (21, RecommendationType.MONITOR),
    (0, RecommendationType.NO_ACTION),
]


@dataclass
class BlockObservation:
    block_id: str
    observation_date: date
    eta: Optional[float] = None
    eto: Optional[float] = None
    kc: Optional[float] = None
    ndvi: Optional[float] = None
    ndvi_previous: Optional[float] = None
    soil_moisture: Optional[float] = None
    soil_moisture_seasonal_avg: Optional[float] = None
    rainfall_forecast: Optional[float] = None
    estimated_irrigation_requirement: Optional[float] = None
    temperature: Optional[float] = None
    phenology_stage: Optional[str] = None


@dataclass
class FeatureContribution:
    metric: str
    raw_value: float
    normalised_value: float
    weight: float
    weighted_score: float
    unit: str = ""
    available: bool = True


@dataclass
class StressResult:
    stress_score: float
    stress_category: StressCategory
    confidence: float
    contributors: list[FeatureContribution]
    model_version: str = "WSM-1.0"
    rules_triggered: list[str] = field(default_factory=list)


def _min_max_normalise(value: float, min_val: float, max_val: float) -> float:
    if max_val == min_val:
        return 0.5
    normalised = (value - min_val) / (max_val - min_val)
    return max(0.0, min(1.0, normalised))


def _calculate_water_deficit(obs: BlockObservation) -> FeatureContribution:
    if obs.eto is None or obs.eta is None:
        return FeatureContribution("water_deficit", 0.0, 0.0, FEATURE_WEIGHTS["water_deficit"], 0.0, "mm", available=False)
    deficit = obs.eto - obs.eta
    normalised = _min_max_normalise(deficit, -5.0, 10.0)
    weight = FEATURE_WEIGHTS["water_deficit"]
    return FeatureContribution("water_deficit", deficit, normalised, weight, normalised * weight, "mm")


def _calculate_et_ratio(obs: BlockObservation) -> FeatureContribution:
    if obs.eto is None or obs.eta is None or obs.eto == 0:
        return FeatureContribution("et_ratio", 0.0, 0.0, FEATURE_WEIGHTS["et_ratio"], 0.0, "ratio", available=False)
    ratio = obs.eta / obs.eto
    normalised = 1.0 - _min_max_normalise(ratio, 0.0, 1.5)
    weight = FEATURE_WEIGHTS["et_ratio"]
    return FeatureContribution("et_ratio", ratio, normalised, weight, normalised * weight, "ratio")


def _calculate_ndvi_trend(obs: BlockObservation) -> FeatureContribution:
    if obs.ndvi is None or obs.ndvi_previous is None:
        return FeatureContribution("ndvi_trend", 0.0, 0.0, FEATURE_WEIGHTS["ndvi_trend"], 0.0, "ndvi", available=False)
    trend = obs.ndvi - obs.ndvi_previous
    normalised = 1.0 - _min_max_normalise(trend, -0.3, 0.3)
    weight = FEATURE_WEIGHTS["ndvi_trend"]
    return FeatureContribution("ndvi_trend", trend, normalised, weight, normalised * weight, "ndvi")


def _calculate_soil_moisture(obs: BlockObservation) -> FeatureContribution:
    if obs.soil_moisture is None:
        return FeatureContribution("soil_moisture", 0.0, 0.0, FEATURE_WEIGHTS["soil_moisture"], 0.0, "index", available=False)
    avg = obs.soil_moisture_seasonal_avg if obs.soil_moisture_seasonal_avg else 50.0
    if avg == 0:
        smi = 0.5
    else:
        smi = obs.soil_moisture / avg
    normalised = 1.0 - _min_max_normalise(smi, 0.0, 1.5)
    weight = FEATURE_WEIGHTS["soil_moisture"]
    return FeatureContribution("soil_moisture_index", smi, normalised, weight, normalised * weight, "index")


def _calculate_rainfall_offset(obs: BlockObservation) -> FeatureContribution:
    rain = obs.rainfall_forecast if obs.rainfall_forecast is not None else 0.0
    irrigation_req = obs.estimated_irrigation_requirement if obs.estimated_irrigation_requirement is not None else 5.0
    offset = rain - irrigation_req
    normalised = 1.0 - _min_max_normalise(offset, -10.0, 10.0)
    weight = FEATURE_WEIGHTS["rainfall_offset"]
    return FeatureContribution("rainfall_offset", offset, normalised, weight, normalised * weight, "mm")


def _calculate_phenology(obs: BlockObservation) -> FeatureContribution:
    stage = obs.phenology_stage.lower() if obs.phenology_stage else "dormancy"
    raw = PHENOLOGY_WEIGHTS.get(stage, 0.5)
    normalised = raw
    weight = FEATURE_WEIGHTS["phenology"]
    return FeatureContribution("phenology_weight", raw, normalised, weight, normalised * weight, "stage")


def calculate_stress(obs: BlockObservation) -> StressResult:
    features = [
        _calculate_water_deficit(obs),
        _calculate_et_ratio(obs),
        _calculate_ndvi_trend(obs),
        _calculate_soil_moisture(obs),
        _calculate_rainfall_offset(obs),
        _calculate_phenology(obs),
    ]

    available_count = sum(1 for f in features if f.available)
    total_count = len(features)

    raw_score = sum(f.weighted_score for f in features)
    stress_score = round(raw_score * 100, 1)
    stress_score = max(0.0, min(100.0, stress_score))

    confidence = _calculate_confidence(features, available_count, total_count, obs)

    category = _score_to_category(stress_score)

    rules_triggered = _determine_rules(stress_score, obs)

    return StressResult(
        stress_score=stress_score,
        stress_category=category,
        confidence=confidence,
        contributors=features,
        rules_triggered=rules_triggered,
    )


def _calculate_confidence(
    features: list[FeatureContribution],
    available_count: int,
    total_count: int,
    obs: BlockObservation,
) -> float:
    data_completeness = available_count / total_count if total_count > 0 else 0.0

    days_old = (date.today() - obs.observation_date).days
    freshness = max(0.0, 1.0 - (days_old / 7.0))

    confidence = (data_completeness * 0.6 + freshness * 0.4)
    return round(max(0.0, min(1.0, confidence)), 2)


def _score_to_category(score: float) -> StressCategory:
    if score <= 20:
        return StressCategory.HEALTHY
    elif score <= 40:
        return StressCategory.MONITOR
    elif score <= 60:
        return StressCategory.MODERATE
    elif score <= 80:
        return StressCategory.HIGH
    else:
        return StressCategory.CRITICAL


def score_to_recommendation(score: float) -> RecommendationType:
    for threshold, rec_type in RECOMMENDATION_THRESHOLDS:
        if score >= threshold:
            return rec_type
    return RecommendationType.NO_ACTION


def _determine_rules(score: float, obs: BlockObservation) -> list[str]:
    rules = []
    if score >= 81:
        rules.append("rule_critical_immediate_irrigation")
    elif score >= 61:
        rules.append("rule_high_stress_tonight")
    elif score >= 41:
        rules.append("rule_moderate_delay")
    elif score >= 21:
        rules.append("rule_monitor")
    else:
        rules.append("rule_healthy_no_action")

    rain = obs.rainfall_forecast if obs.rainfall_forecast is not None else 0.0
    if rain > 5.0 and score < 70:
        rules.append("rule_rain_expected_hold")

    if obs.phenology_stage and obs.phenology_stage.lower() in ("veraison", "flowering"):
        rules.append("rule_sensitive_growth_stage")

    return rules


def generate_explanation(stress: StressResult, recommendation: RecommendationType) -> str:
    parts = []
    parts.append(f"Water Stress Score: {stress.stress_score}/100 ({stress.stress_category.value})")

    available_features = [c for c in stress.contributors if c.available]
    if available_features:
        top_factors = sorted(available_features, key=lambda c: c.weighted_score, reverse=True)[:3]
        factor_descriptions = []
        for f in top_factors:
            if f.weighted_score > 0.15:
                factor_descriptions.append(f"{f.metric} ({f.raw_value:.2f} {f.unit})")
        if factor_descriptions:
            parts.append(f"Key contributing factors: {', '.join(factor_descriptions)}")

    parts.append(f"Recommendation: {recommendation.value.replace('_', ' ').title()}")
    parts.append(f"Confidence: {stress.confidence * 100:.0f}%")

    return ". ".join(parts) + "."
