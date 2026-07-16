# VineMind AI
# Database Design Specification

---

| Property | Value |
|----------|-------|
| Document ID | VM-009 |
| Version | 1.0 |
| Status | Draft |
| Standard | Database Architecture Specification |
| Project | VineMind AI |
| Author | Jeffrey Moepi |
| Last Updated | 16 July 2026 |
| Related Documents | VM-004 Data Architecture, VM-006 Decision Intelligence Engine, VM-008 API Specification |

---

# Table of Contents

1. Introduction
2. Database Philosophy
3. Technology Stack
4. Database Architecture
5. Core Domain Model
6. Entity Relationships
7. Schema Design
8. Geospatial Data
9. Time-Series Strategy
10. Decision Evidence Storage
11. Indexing Strategy
12. Data Integrity
13. Backup & Recovery
14. Scalability
15. Security
16. Future Evolution

---

# 1. Introduction

The VineMind database stores environmental observations, vineyard metadata, irrigation recommendations and historical decision records.

The design prioritises:

- Data integrity
- Geospatial performance
- Historical traceability
- Explainability
- Scalability

The database serves as the persistent storage layer for the Decision Intelligence Platform.

---

# 2. Database Philosophy

The database is designed around four principles.

## Single Source of Truth

Every vineyard observation exists once.

---

## Immutable Decisions

Historical recommendations are never overwritten.

New recommendations create new records.

---

## Geospatial First

Spatial queries are first-class operations.

---

## Explainability

Every recommendation stores its supporting evidence.

---

# 3. Technology Stack

| Component | Technology |
|-----------|------------|
| Database | PostgreSQL 16 |
| Spatial Extension | PostGIS |
| ORM | Prisma |
| Cache | Redis |
| Object Storage | Cloud Storage (future) |

---

# 4. Database Architecture

```text
React Dashboard
        │
REST API
        │
Decision Intelligence Engine
        │
──────────────
PostgreSQL
        │
 ├── Vineyard Data
 ├── Weather
 ├── Observations
 ├── Recommendations
 ├── Decision Evidence
 ├── Users
 └── Audit Logs
```

---

# 5. Core Domain Model

The primary entities include:

- Users
- Vineyards
- Vineyard Blocks
- Daily Observations
- Weather Records
- Water Stress Scores
- Recommendations
- Decision Evidence Packages
- Alerts
- Reports

---

# 6. Entity Relationships

```text
User
 │
 ├── Vineyards
 │
 │     ├── Blocks
 │     │      ├── Observations
 │     │      ├── Water Stress Scores
 │     │      ├── Recommendations
 │     │      └── Decision Evidence
 │
 └── Reports
```

---

# 7. Schema Design

## Users

```text
User
-----
id
name
email
password_hash
role
created_at
```

---

## Vineyards

```text
Vineyard
---------
id
name
location
owner
created_at
```

---

## Vineyard Blocks

```text
Block
------
id
vineyard_id
name
cultivar
area_ha
geometry
created_at
```

---

## Daily Observations

```text
Observation
------------
id
block_id
date
eta
eto
kc
ndvi
soil_moisture
temperature
rainfall
phenology_stage
```

---

## Water Stress Scores

```text
StressScore
------------
id
block_id
observation_id
score
category
confidence
model_version
generated_at
```

---

## Recommendations

```text
Recommendation
---------------
id
stress_score_id
priority
recommendation
status
generated_at
```

---

## Decision Evidence Package

```text
DecisionEvidence
----------------
id
recommendation_id
contributors_json
confidence
model_version
generated_at
```

---

# 8. Geospatial Data

Every vineyard block stores a PostGIS geometry.

```sql
geometry(POLYGON,4326)
```

This enables:

- Spatial joins
- Area calculations
- Neighbour searches
- Map rendering
- Satellite overlays

---

# 9. Time-Series Strategy

Environmental observations are append-only.

Each observation represents a snapshot in time.

Historical data is never updated.

```text
Block A12

2026-07-12

↓

2026-07-13

↓

2026-07-14

↓

2026-07-15
```

This enables trend analysis and reproducible historical recommendations.

---

# 10. Decision Evidence Storage

Each recommendation stores a complete Decision Evidence Package.

Example:

```json
{
  "stress_score":82,
  "confidence":0.94,
  "contributors":[
    "Water Deficit",
    "NDVI",
    "Phenology",
    "Rain Forecast"
  ]
}
```

This allows every recommendation to be audited and explained months or years later.

---

# 11. Indexing Strategy

Indexes should be created for:

- Primary keys
- Foreign keys
- Observation date
- Block identifier
- Stress score
- Recommendation status
- PostGIS geometry

Spatial indexes use GiST indexes for efficient map-based queries.

---

# 12. Data Integrity

The database enforces:

- Primary keys
- Foreign keys
- NOT NULL constraints
- Unique constraints
- Check constraints
- Cascading rules where appropriate

Business logic remains in the application layer.

---

# 13. Backup & Recovery

Recommended strategy:

- Daily full backup
- Hourly incremental backup
- Point-in-time recovery
- Off-site encrypted storage

Recovery objectives:

| Metric | Target |
|--------|--------|
| RPO | < 1 hour |
| RTO | < 4 hours |

---

# 14. Scalability

Future improvements include:

- Read replicas
- Table partitioning by season
- TimescaleDB for high-volume time-series data
- Redis caching
- Object storage for imagery

---

# 15. Security

Security controls include:

- Encryption at rest
- TLS in transit
- Role-Based Access Control
- Row-level security (future)
- Audit logging
- Secret management via environment variables

---

# 16. Future Evolution

The schema is designed to support:

- IoT sensor streams
- Drone imagery
- Machine learning features
- Multi-farm deployments
- Multi-tenant SaaS
- Climate simulations
- Carbon footprint analytics

---

# Appendix A
## Database Layers

```text
Presentation Layer

↓

REST API

↓

Domain Services

↓

Repository Layer

↓

PostgreSQL + PostGIS
```

---

# Appendix B
## Storage Responsibilities

| Entity | Responsibility |
|---------|----------------|
| Observation | Raw environmental measurements |
| StressScore | Scientific assessment |
| Recommendation | Operational decision |
| DecisionEvidence | Explainability |
| Alert | Notifications |
| AuditLog | Compliance |

---

# Conclusion

The VineMind database has been designed as a geospatial, time-series and decision-oriented data platform. By separating observations, scientific assessments, operational recommendations and Decision Evidence Packages, the architecture preserves historical integrity while supporting explainability, scalability and future expansion into enterprise-grade precision agriculture.