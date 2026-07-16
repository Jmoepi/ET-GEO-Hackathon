# VineMind AI
# Water Stress Model Specification

---

| Property | Value |
|----------|-------|
| Document ID | VM-007 |
| Version | 1.0 |
| Status | Draft |
| Standard | Scientific Decision Model Specification |
| Project | VineMind AI |
| Author | Jeffrey Moepi |
| Last Updated | 16 July 2026 |
| Related Documents | VM-004 Data Architecture, VM-005 Geospatial Processing Pipeline, VM-006 Decision Intelligence Engine |

---

# Table of Contents

1. Introduction
2. Purpose
3. Design Principles
4. Scientific Background
5. Model Inputs
6. Feature Engineering
7. Feature Normalisation
8. Feature Weighting
9. Water Stress Score Calculation
10. Confidence Calculation
11. Stress Categories
12. Decision Thresholds
13. Decision Evidence Package
14. Explainability
15. Validation Strategy
16. Model Versioning
17. Limitations
18. Future Evolution

---

# 1. Introduction

The Water Stress Model is the scientific core of VineMind AI.

Its responsibility is to transform environmental observations into a reproducible and explainable Water Stress Score that represents the irrigation urgency of an individual vineyard block.

The model is intentionally deterministic.

Identical inputs always produce identical outputs.

The model itself does not generate irrigation recommendations.

Instead, it provides the quantitative assessment consumed by the Decision Intelligence Engine.

---

# 2. Purpose

The Water Stress Model exists to answer one question:

> **How stressed is this vineyard block today?**

To answer this question, the model combines multiple environmental indicators into a single stress score representing the current physiological condition of the vineyard.

The resulting score enables consistent irrigation decisions across all vineyard blocks.

---

# 3. Design Principles

The model follows six guiding principles.

## Scientific Transparency

Every calculation must be explainable.

---

## Deterministic Behaviour

The same input data always produces the same score.

---

## Explainability

Every score must identify the variables that contributed to it.

---

## Modularity

Variables and weights can be updated without redesigning the system.

---

## Reproducibility

Historical calculations can be reproduced from archived datasets.

---

## Extensibility

Future machine learning models can replace individual components without changing the platform architecture.

---

# 4. Scientific Background

Plant water stress cannot be measured using a single observation.

Instead, stress emerges from the interaction of multiple environmental factors including:

- Actual Evapotranspiration (ETa)
- Reference Evapotranspiration (ETo)
- Crop Coefficient (Kc)
- Vegetation Health (NDVI)
- Soil Moisture
- Rainfall Forecast
- Air Temperature
- Vineyard Phenology

The Water Stress Model combines these variables into a single numerical representation of irrigation urgency.

---

# 5. Model Inputs

| Variable | Description | Source |
|----------|-------------|--------|
| ETa | Actual evapotranspiration | ET-GEO |
| ETo | Reference evapotranspiration | ET-GEO |
| Kc | Crop coefficient | ET-GEO |
| NDVI | Vegetation health | Sentinel-2 |
| Soil Moisture | Available water | ET-GEO |
| Rain Forecast | Expected rainfall | OpenWeather |
| Temperature | Forecast temperature | OpenWeather |
| Phenology Stage | Vineyard growth stage | ET-GEO |

---

# 6. Feature Engineering

Raw observations are transformed into analytical features.

## Water Deficit

```text
Water Deficit = ETo − ETa
```

Represents unmet atmospheric water demand.

---

## ET Ratio

```text
ET Ratio = ETa / ETo
```

Measures how effectively the vineyard is meeting evaporative demand.

---

## NDVI Trend

```text
Current NDVI − Previous NDVI
```

Represents changes in canopy health.

---

## Soil Moisture Index

```text
Current Moisture / Seasonal Average
```

Provides relative water availability.

---

## Rainfall Offset

```text
Forecast Rainfall − Estimated Irrigation Requirement
```

Determines whether expected rainfall may satisfy water demand.

---

## Phenology Weight

Growth stages influence irrigation sensitivity.

Example:

| Stage | Weight |
|--------|---------|
| Bud Break | Medium |
| Flowering | High |
| Fruit Set | High |
| Veraison | Critical |
| Ripening | High |
| Harvest | Low |

---

# 7. Feature Normalisation

To combine variables measured in different units, each feature is normalised to a common scale between 0 and 1.

General formula:

```text
Normalised Value =
(Current − Minimum)
/
(Maximum − Minimum)
```

Normalisation prevents any single feature from dominating the final score solely because of its measurement scale.

---

# 8. Feature Weighting

Each feature contributes differently to vineyard water stress.

Example Version 1.0 weights:

| Feature | Weight |
|----------|--------|
| Water Deficit | 30% |
| ET Ratio | 20% |
| Soil Moisture | 20% |
| NDVI Trend | 15% |
| Rain Forecast | 10% |
| Phenology Adjustment | 5% |

Weights are configurable and may be refined through expert feedback or validation studies.

---

# 9. Water Stress Score Calculation

The Water Stress Score is calculated using a weighted linear model.

```text
Stress Score =
Σ (Normalised Feature × Weight)
```

The resulting value is scaled to a score between 0 and 100.

Example:

| Feature | Weighted Contribution |
|----------|----------------------|
| Water Deficit | 24 |
| ET Ratio | 16 |
| Soil Moisture | 15 |
| NDVI Trend | 12 |
| Rain Forecast | 8 |
| Phenology | 5 |

Total Water Stress Score:

```text
80
```

---

# 10. Confidence Calculation

The model also produces a confidence score indicating the reliability of the recommendation.

Confidence is influenced by:

- Dataset completeness
- Data freshness
- Weather reliability
- Missing observations
- Sensor quality
- Spatial coverage

Example:

| Confidence | Interpretation |
|-------------|----------------|
| 95–100% | Very High |
| 85–94% | High |
| 70–84% | Moderate |
| <70% | Low |

Confidence does not affect the Water Stress Score itself but informs users about the quality of the underlying evidence.

---

# 11. Stress Categories

| Score | Category | Interpretation |
|--------|----------|----------------|
| 0–20 | Healthy | No irrigation required |
| 21–40 | Monitor | Continue observation |
| 41–60 | Moderate | Prepare irrigation |
| 61–80 | High | Irrigation recommended |
| 81–100 | Critical | Immediate irrigation required |

These categories are consumed by the Decision Intelligence Engine.

---

# 12. Decision Thresholds

The Water Stress Model produces a score only.

Operational recommendations are assigned by the Decision Intelligence Engine.

Example mapping:

| Stress Score | Recommendation |
|--------------|----------------|
| 0–20 | No Action |
| 21–40 | Monitor |
| 41–60 | Prepare Irrigation |
| 61–80 | Irrigate Within 24 Hours |
| 81–100 | Irrigate Immediately |

---

# 13. Decision Evidence Package (DEP)

Every Water Stress calculation produces a structured Decision Evidence Package.

Example:

```json
{
  "decision_id": "DEP-20260716-A12",
  "block_id": "A12",
  "stress_score": 82,
  "confidence": 0.94,
  "contributors": [
    {
      "metric": "Water Deficit",
      "value": 1.4,
      "unit": "mm"
    },
    {
      "metric": "NDVI Trend",
      "value": "Declining"
    },
    {
      "metric": "Rain Forecast",
      "value": 0,
      "unit": "mm"
    },
    {
      "metric": "Phenology",
      "value": "Veraison"
    }
  ],
  "model_version": "WSM-1.0"
}
```

The Decision Evidence Package is consumed by:

- Decision Intelligence Engine
- REST API
- Dashboard
- Explainable AI Copilot
- Reporting Services

---

# 14. Explainability

Every Water Stress Score must include:

- Input variables
- Feature values
- Applied weights
- Final score
- Confidence
- Model version
- Timestamp

This enables complete traceability and auditability.

---

# 15. Validation Strategy

The model should be validated using:

- Historical ET-GEO datasets
- Agronomist review
- Vineyard manager feedback
- Sensitivity analysis
- Cross-season comparisons
- Regression testing after model updates

Validation results should be documented before introducing new model versions.

---

# 16. Model Versioning

The Water Stress Model follows semantic versioning.

| Version | Description |
|----------|-------------|
| WSM-1.0 | Initial weighted rule-based model |
| WSM-1.1 | Weight refinements |
| WSM-2.0 | Machine learning assisted scoring |
| WSM-3.0 | Hybrid AI and agronomic model |

Every recommendation stores the model version used to generate it.

---

# 17. Limitations

Current limitations include:

- Dependence on data quality
- Limited real-time sensor integration
- Weather forecast uncertainty
- Static feature weights in Version 1.0
- Rule-based rather than adaptive learning

These limitations are acknowledged to ensure transparent interpretation of model outputs.

---

# 18. Future Evolution

Future enhancements may include:

- Dynamic feature weighting
- Machine learning optimisation
- Reinforcement learning for irrigation scheduling
- Predictive water demand forecasting
- Climate anomaly detection
- Digital twin vineyard simulation
- Continuous calibration using sensor feedback

The architecture has been designed so these capabilities can be introduced without changing downstream systems.

---

# Appendix A
## Model Workflow

```text
Environmental Observations
        │
        ▼
Feature Engineering
        │
        ▼
Normalisation
        │
        ▼
Weighted Scoring
        │
        ▼
Water Stress Score
        │
        ▼
Confidence Calculation
        │
        ▼
Decision Evidence Package
        │
        ▼
Decision Intelligence Engine
```

---

# Appendix B
## Mathematical Summary

```text
Stress Score =
Σ(Normalised Feature × Weight)

↓

Scale to 0–100

↓

Assign Stress Category

↓

Generate Decision Evidence Package

↓

Pass to Decision Intelligence Engine
```

---

# Conclusion

The Water Stress Model provides the scientific foundation for VineMind AI by transforming geospatial, environmental, and phenological observations into a transparent and reproducible Water Stress Score.

By separating scientific scoring from operational decision-making, the platform ensures that irrigation recommendations remain explainable, auditable, and easy to evolve as new data sources and modelling techniques become available. This architecture supports both the immediate goals of the ET-GEO Hackathon and the long-term vision of a production-grade precision irrigation decision-support platform.