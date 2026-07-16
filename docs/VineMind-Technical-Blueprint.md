```
Document ID:    VM-099
Document:       Technical Blueprint
Project:        VineMind AI
Version:        1.0
Status:         Draft
Author:         Jeffrey Moepi
Hackathon:      TerraClim ET-GEO Hackathon 2026
Last Updated:   16 July 2026
```

---

# VineMind AI — Technical Blueprint

## Executive Summary

VineMind AI is an intelligent vineyard irrigation decision-support platform that transforms TerraClim ET-GEO evapotranspiration data into clear, explainable, prioritised irrigation recommendations for vineyard managers. Rather than a traditional GIS dashboard, it acts as a digital agronomic assistant — interpreting satellite observations, environmental conditions, and vineyard characteristics to recommend practical irrigation actions at the vineyard-block level.

**Core Problem:** Current irrigation workflows are data-driven rather than decision-driven. Datasets (ETa, ETo, Kc, NDVI, soil moisture, phenology, weather) rarely answer the operational question: *"Which vineyard blocks should I irrigate today, how much water, and why?"*

**Core Innovation:** A deterministic Water Stress Model that produces reproducible, fully explainable scores, paired with an Explainable AI Copilot that interprets recommendations without ever generating incorrect advice.

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │  Web App     │  │  Mobile App  │  (Future)                   │
│  │  (React 19)  │  │  (React Nat.)│                             │
│  └──────┬───────┘  └──────┬───────┘                             │
└─────────┼──────────────────┼────────────────────────────────────┘
          │ HTTPS / REST     │
┌─────────┼──────────────────┼────────────────────────────────────┐
│         ▼                  ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              REST API (FastAPI, Python 3.11+)             │   │
│  │  Auth │ Vineyard │ Recommendation │ Weather │ Copilot     │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│  ┌──────────────────────────┼───────────────────────────────┐   │
│  │          DECISION INTELLIGENCE ENGINE                      │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐ │   │
│  │  │ Context   │ │  Water    │ │ Priority  │ │ Explain  │ │   │
│  │  │  Engine   │ │  Stress   │ │  Engine   │ │  Engine  │ │   │
│  │  │           │ │  Model    │ │           │ │          │ │   │
│  │  │           │ │ (WSM-1.0) │ │           │ │  (DEP)   │ │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └──────────┘ │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│  ┌──────────────────────────┼───────────────────────────────┐   │
│  │         GEOSPATIAL PROCESSING PIPELINE                    │   │
│  │  Rasterio │ GeoPandas │ Shapely │ NumPy │ PostGIS         │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│  ┌──────────────────────────┼───────────────────────────────┐   │
│  │                      DATA LAYER                            │   │
│  │  PostgreSQL 16 + PostGIS │ Redis (Future)                  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Architectural Principles

| Principle | Description |
|-----------|-------------|
| Separation of Concerns | UI, API, Domain Logic, and Data are strictly separated |
| Explainability | No black boxes — every recommendation traces to input data and rules |
| Deterministic Decisioning | Same inputs always produce the same Water Stress Score |
| API First | All functionality accessible via REST API |
| Data Driven | Decisions based on multi-source EO and environmental data |
| Cloud Native | Docker containerisation, managed platform deployment |

---

## 2. Data Architecture

### 2.1 Data Sources

| Source | Format | Content | Provider |
|--------|--------|---------|----------|
| ETa | GeoTIFF | Actual evapotranspiration | TerraClim ET-GEO |
| ETo | GeoTIFF | Reference evapotranspiration | TerraClim ET-GEO |
| Kc | GeoTIFF | Crop coefficient | TerraClim ET-GEO |
| NDVI | GeoTIFF | Normalised Difference Vegetation Index | Sentinel-2 |
| Vineyard Blocks | Shapefile / GeoPackage | Block boundaries (polygons) | User upload |
| Phenology | CSV / Excel | Growth stage per block | User input |
| Soil Moisture | CSV / Raster | Soil moisture readings | User input / sensors |
| Weather | REST API (JSON) | Temperature, rainfall, humidity, forecast | OpenWeather API |

### 2.2 Data Classification

| Level | Type | Examples |
|-------|------|----------|
| L1 — Raw | Original files (immutable) | GeoTIFF, Shapefile, CSV |
| L2 — Processed | Block-aggregated values | Mean ETa, NDVI, Soil Moisture per block per day |
| L3 — Derived | Analytical outputs | Water Stress Score, Recommendation, Confidence, Priority |
| L4 — Presentation | User-facing views | Dashboard widgets, charts, map overlays, reports |

### 2.3 Geospatial Pipeline Flow

```
ET-GEO Data Pack → Validate Files → Load Polygons → Load Raster → CRS Alignment
→ Clip to Blocks → Calculate Statistics → Feature Engineering → Water Stress Scoring
→ Recommendation → Persist to PostgreSQL → Serve via API → Display on Dashboard
```

### 2.4 Feature Engineering

| Feature | Formula | Weight |
|---------|---------|--------|
| Water Deficit | ETo − ETa | 30% |
| ET Ratio | ETa / ETo | 20% |
| Soil Moisture Index | Current / Seasonal Average | 20% |
| NDVI Trend | Current NDVI − Previous NDVI | 15% |
| Rainfall Offset | Forecast Rain − Estimated Requirement | 10% |
| Phenology Weight | Bud Break:Medium, Flowering:High, Veraison:Critical, etc. | 5% |

---

## 3. Decision Intelligence Engine

### 3.1 Water Stress Model (WSM-1.0)

```
Stress Score = Σ(Normalised_Feature_i × Weight_i) × 100
```

**Normalisation:** Each feature scaled to 0–1 using min-max normalisation.

**Output:** Water Stress Score (0–100) with category assignment:

| Score Range | Category | Colour | Action |
|-------------|----------|--------|--------|
| 0–20 | Healthy | Green | No Action Required |
| 21–40 | Monitor | Yellow | Monitor Tomorrow |
| 41–60 | Moderate | Orange | Delay Irrigation |
| 61–80 | High Stress | Red | Irrigate Tonight |
| 81–100 | Critical | Dark Red | Irrigate Immediately |

### 3.2 Confidence Scoring

Confidence reflects data quality and completeness:

| Level | Range | Conditions |
|-------|-------|------------|
| Very High | 95–100% | All data present, recent, reliable |
| High | 85–94% | Minor gaps, acceptable quality |
| Moderate | 70–84% | Some missing data, fallback values used |
| Low | <70% | Significant uncertainty, missing observations |

### 3.3 Decision Evidence Package (DEP)

Every recommendation stores a complete audit trail:

```json
{
  "decision_id": "dec_20260716_blkA",
  "block_id": "blk_abc123",
  "date": "2026-07-16",
  "stress_score": 74,
  "stress_category": "high_stress",
  "confidence": 0.87,
  "model_version": "WSM-1.0",
  "contributors": [
    {"metric": "water_deficit", "value": 4.2, "unit": "mm", "normalised": 0.84, "weight": 0.30},
    {"metric": "et_ratio", "value": 0.82, "unit": "ratio", "normalised": 0.72, "weight": 0.20},
    {"metric": "soil_moisture_index", "value": 0.61, "unit": "index", "normalised": 0.68, "weight": 0.20},
    {"metric": "ndvi_trend", "value": -0.08, "unit": "ndvi", "normalised": 0.71, "weight": 0.15},
    {"metric": "rainfall_offset", "value": 0.0, "unit": "mm", "normalised": 0.95, "weight": 0.10},
    {"metric": "phenology_weight", "value": "veraison", "unit": "stage", "normalised": 0.90, "weight": 0.05}
  ],
  "decision_rules_triggered": ["rule_high_stress_no_rain"],
  "recommendation": "irrigate_tonight",
  "explanation": "Block A shows high water stress (Score 74/100) due to significant water deficit of 4.2mm, declining NDVI trend, below-average soil moisture, no rainfall expected, and veraison growth stage which is highly sensitive to water stress."
}
```

### 3.4 Recommendation State Machine

```
Generated → Pending → Accepted → Completed
                   → Dismissed → (archived)
                   → Expired → (archived)
```

---

## 4. Technology Stack

### 4.1 Core Technologies

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React + TypeScript | 19.x | Component ecosystem, type safety |
| Build Tool | Vite | 5.x | Fast development, optimised builds |
| Styling | Tailwind CSS + shadcn/ui | — | Rapid UI development |
| Mapping | Mapbox GL JS | — | Satellite imagery, vector rendering |
| Charts | Recharts | — | React-native data visualisation |
| State (Server) | TanStack Query | 5.x | Server state caching |
| State (UI) | Zustand | 4.x | Lightweight UI state |
| Backend | FastAPI | 0.110+ | Async Python, auto OpenAPI docs |
| ORM | Prisma | — | Type-safe database access |
| Database | PostgreSQL + PostGIS | 16+ | Spatial + relational data |
| Cache | Redis | 7.x | Session, weather cache (future) |
| Geospatial | Rasterio, GeoPandas, Shapely | — | Raster/vector processing |
| AI/LLM | Azure OpenAI | — | Explainable AI Copilot |

### 4.2 Justification (ADR Summary)

| Decision | ADR | Rationale |
|----------|-----|-----------|
| FastAPI | ADR-001 | Async Python, auto-docs, scientific ecosystem |
| PostgreSQL + PostGIS | ADR-002 | Spatial + relational, mature, reliable |
| React + TypeScript | ADR-003 | Ecosystem, type safety, mapping support |
| Deterministic Model | ADR-004 | Explainable, reproducible, no training data needed |
| Decision Evidence Package | ADR-005 | Auditability, single source of truth |
| Read-Only AI Copilot | ADR-006 | Safety, deterministic decisions, trust |
| Docker Compose | ADR-007 | Consistent environments, simple demo |
| Append-Only Data | ADR-008 | Audit trail, reliable historical analysis |
| URI Versioning | ADR-009 | Clear API evolution, explicit contract |
| Mapbox GL JS | ADR-010 | High performance, satellite imagery, React support |

---

## 5. Database Schema

### 5.1 Entity Relationship Diagram

See `docs/diagrams/erd.mmd` for the complete ERD.

### 5.2 Core Tables

**Users**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| name | VARCHAR(255) | NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| role | VARCHAR(20) | DEFAULT 'viewer' |
| preferences | JSONB | DEFAULT '{}' |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |

**Vineyards**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| name | VARCHAR(255) | NOT NULL |
| owner_id | UUID | FK → Users |
| location | GEOGRAPHY(POINT, 4326) | — |
| boundary | GEOGRAPHY(POLYGON, 4326) | — |
| area_hectares | DECIMAL(10,2) | — |
| metadata | JSONB | DEFAULT '{}' |

**Vineyard Blocks**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| vineyard_id | UUID | FK → Vineyards |
| name | VARCHAR(255) | NOT NULL |
| cultivar | VARCHAR(100) | — |
| area_ha | DECIMAL(10,2) | — |
| geometry | GEOGRAPHY(POLYGON, 4326) | — |
| planting_year | VARCHAR(10) | — |

**Daily Observations** (append-only)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| block_id | UUID | FK → Blocks |
| observation_date | DATE | NOT NULL |
| eta | DECIMAL | — |
| eto | DECIMAL | — |
| kc | DECIMAL | — |
| ndvi | DECIMAL | — |
| soil_moisture | DECIMAL | — |
| temperature | DECIMAL | — |
| rainfall | DECIMAL | — |
| phenology_stage | VARCHAR(50) | — |
| data_source | VARCHAR(100) | — |

**Water Stress Scores**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| observation_id | UUID | FK → Observations |
| block_id | UUID | FK → Blocks |
| stress_score | DECIMAL | 0–100 |
| stress_category | VARCHAR(20) | — |
| confidence | DECIMAL | 0–1 |
| model_version | VARCHAR(20) | e.g. 'WSM-1.0' |
| contributors | JSONB | — |

**Recommendations** (append-only)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| stress_score_id | UUID | FK → Stress Scores |
| block_id | UUID | FK → Blocks |
| recommendation_type | VARCHAR(50) | — |
| priority | VARCHAR(20) | — |
| status | VARCHAR(20) | DEFAULT 'pending' |
| explanation | TEXT | — |
| confidence | DECIMAL | — |

**Decision Evidence**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| recommendation_id | UUID | FK → Recommendations |
| contributors_json | JSONB | Full feature breakdown |
| stress_score | DECIMAL | — |
| confidence | DECIMAL | — |
| model_version | VARCHAR(20) | — |

---

## 6. API Specification

### 6.1 Base URL

- Production: `https://api.vinemind.ai/api/v1`
- Local: `http://localhost:8000/api/v1`

### 6.2 Authentication

JWT Bearer token: `Authorization: Bearer <token>`

### 6.3 Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | Authenticate and receive JWT |
| GET | /vineyards | List all vineyards |
| GET | /vineyards/{id} | Get vineyard details |
| GET | /blocks | List all blocks |
| GET | /blocks/{id} | Get block details |
| GET | /stress/{blockId} | Get current water stress score |
| GET | /stress/history/{blockId} | Get historical stress scores |
| GET | /recommendations | List recommendations |
| GET | /recommendations/{blockId} | Get recommendation for block |
| GET | /evidence/{blockId} | Get Decision Evidence Package |
| POST | /copilot/chat | Ask AI Copilot a question |

### 6.4 Performance Targets

| Metric | Target |
|--------|--------|
| Average response time | < 300ms |
| P95 response time | < 800ms |
| Concurrent users | 500+ |
| Availability | 99.9% |

---

## 7. AI Governance & Explainability

### 7.1 AI Philosophy

1. **Explain recommendations** — never replace expertise
2. **Never invent agronomic advice** — AI consumes DEPs, never generates decisions
3. **Stay grounded** — every response references verified platform data
4. **Be honest** — acknowledge uncertainty, missing data, limitations
5. **Keep humans in control** — final irrigation decision belongs to the grower

### 7.2 AI Boundaries

| Responsibility | Decision Engine | AI Copilot |
|----------------|----------------|------------|
| Calculate Water Stress Score | YES | NO |
| Generate Recommendation | YES | NO |
| Explain Recommendation | NO | YES |
| Compare Blocks | NO | YES |
| Summarise Trends | NO | YES |
| Execute Irrigation | NO | NO |

### 7.3 Prompt Governance

```
User Question → Prompt Validation → Retrieve DEP from Database
→ Build Context with Evidence → Generate LLM Prompt
→ Validate Response → Return to User
```

Only verified, contextual information reaches the LLM. No autonomous data generation.

---

## 8. Frontend Architecture

### 8.1 Application Structure

```
src/
├── app/                  # App shell, routing, providers
├── pages/
│   ├── Dashboard         # Health overview, priorities, weather
│   ├── VineyardExplorer  # Interactive map with stress overlays
│   ├── BlockDetails      # ETa, ETo, NDVI, stress, recommendation
│   ├── DecisionCentre    # Irrigation priorities, evidence
│   ├── Analytics         # Historical trends, comparisons
│   ├── Reports           # Downloadable PDF reports
│   └── AICopilot         # Conversational interface
├── components/
│   ├── map/              # Map, overlays, layer controls
│   ├── charts/           # ETa, NDVI, stress trend charts
│   ├── cards/            # Metric, recommendation, weather cards
│   └── copilot/          # Chat panel, evidence display
├── hooks/
├── services/             # API client functions
├── state/                # Zustand stores
└── utils/
```

### 8.2 Design System

| Stress Category | Colour | Hex |
|-----------------|--------|-----|
| Healthy | Green | #22C55E |
| Monitor | Yellow | #EAB308 |
| Moderate | Orange | #F97316 |
| High Stress | Red | #EF4444 |
| Critical | Dark Red | #DC2626 |
| No Data | Grey | #9CA3AF |

### 8.3 Performance Targets

| Metric | Target |
|--------|--------|
| Initial load | < 2s |
| Map render | < 1s |
| API updates | < 300ms |
| Lighthouse score | > 95 |

---

## 9. Deployment Architecture

### 9.1 Environments

| Environment | Infrastructure | Purpose |
|-------------|----------------|---------|
| Local | Docker Compose | Development |
| Staging | Vercel (FE) + Railway (BE) + Managed PG | Testing |
| Production | Vercel + Railway + Managed PG | Live |
| Demo | Docker Compose on single VM | Hackathon presentations |

### 9.2 CI/CD Pipeline

```
Developer Push → GitHub → Run Tests → Lint & Format → Build
→ Security Checks → Deploy (Staging auto / Production manual) → Health Check
```

### 9.3 Infrastructure Cost (MVP)

| Component | Monthly Cost (ZAR) |
|-----------|-------------------|
| Frontend (Vercel free tier) | R 0 |
| Backend (Railway free tier) | R 0 |
| PostgreSQL (managed) | R 500 |
| Mapbox (free tier) | R 0 |
| OpenWeather (free tier) | R 0 |
| Domain | R 17/month |
| **Total** | **~R 517/month** |

---

## 10. Security Architecture

| Layer | Measure | Implementation |
|-------|---------|----------------|
| Transport | TLS 1.3 | Platform-managed certificates |
| Authentication | JWT | FastAPI + Argon2id password hashing |
| Authorisation | RBAC | Application-level (Admin/Manager/Agronomist/Viewer) |
| API | Rate limiting, input validation | FastAPI middleware |
| Data | Encryption at rest | Managed database |
| AI Copilot | Prompt sanitisation, grounded responses | Input validation + DEP-only context |
| Audit | Immutable audit logs | Application-level logging |

---

## 11. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ET-GEO data unavailable | Medium | High | Cache previous observations, use fallback values |
| Weather API downtime | Medium | Medium | 7-day forecast cache, seasonal averages fallback |
| LLM API issues | Medium | Low | Copilot degrades to showing DEP data directly |
| Missing imagery (cloud cover) | High | Medium | Use previous valid NDVI, flag reduced confidence |
| Water Stress Model accuracy | Medium | High | Expert validation, weight tuning, future ML upgrade |
| Data breach | Low | Critical | Encryption, RBAC, audit logging |

---

## 12. Success Metrics

### 12.1 Technical

| Metric | Target |
|--------|--------|
| Test coverage | > 90% (backend), > 80% (frontend) |
| API availability | 99.5% |
| API response time (p95) | < 800ms |
| Dashboard load time | < 2s |
| Water Stress Model | 100% deterministic (same inputs → same output) |

### 12.2 Agricultural Impact

| Metric | Target |
|--------|--------|
| Recommendation acceptance rate | > 70% |
| Water savings vs. unmanaged | > 20% |
| Decision time reduction | > 50% (from hours to minutes) |
| Stress detection lead time | > 48 hours before visible symptoms |

---

## Appendix A: Documentation Index

| Doc ID | Title | File |
|--------|-------|------|
| VM-000 | Executive Summary | `00-Executive-Summary.md` |
| VM-001 | Product Vision | `01-Product-Vision.md` |
| VM-002 | Requirements Specification | `02-Requirements-Specification.md` |
| VM-003 | System Architecture | `03-System-Architecture.md` |
| VM-004 | Data Architecture | `04-Data-Architecture.md` |
| VM-005 | Geospatial Pipeline | `05-Geospatial-Pipeline.md` |
| VM-006 | Recommendation Engine | `06-Recommendation-Engine.md` |
| VM-007a | AI Copilot Architecture | `07-AI-Copilot-Architecture.md` |
| VM-007b | Water Stress Model | `07-Water-Stress-Model.md` |
| VM-008 | API Specification | `08-API-Specification.md` |
| VM-009 | Database Design | `09-Database-Design.md` |
| VM-010 | Frontend Architecture | `10-Frontend-Architecture.md` |
| VM-011 | Backend / Security Architecture | `11-Backend-Architecture.md` |
| VM-012 | Deployment Guide | `12-Deployment-Guide.md` |
| VM-013 | Testing Strategy | `13-Testing-Strategy.md` |
| VM-014 | Development Roadmap | `14-Development-Roadmap.md` |
| VM-015 | AI Governance & Explainability | `15-AI-Governance-Explainability.md` |
| VM-015a | Submission Strategy | `15-Submission-Strategy.md` |
| VM-016 | Operations & Monitoring | `16-Operations-Monitoring.md` |
| VM-017 | Architecture Decision Records | `17-Architecture-Decision-Records.md` |
| VM-099 | Technical Blueprint (this document) | `VineMind-Technical-Blueprint.md` |

## Appendix B: Architecture Diagrams

| Diagram | File | Description |
|---------|------|-------------|
| System Context (C4 L1) | `diagrams/context-diagram.mmd` | People, system, external systems |
| Container (C4 L2) | `diagrams/c4-container.mmd` | Frontend, backend, data containers |
| Component (C4 L3) | `diagrams/c4-component.mmd` | Internal components of each service |
| Data Pipeline | `diagrams/data-pipeline.mmd` | End-to-end data processing flow |
| Recommendation Flow | `diagrams/recommendation-flow.mmd` | How recommendations are generated |
| Recommendation Sequence | `diagrams/recommendation-sequence.mmd` | User interaction sequence diagram |
| Ingestion Pipeline | `diagrams/ingestion-pipeline.mmd` | Data ingestion and validation |
| Deployment | `diagrams/deployment.mmd` | Infrastructure and deployment topology |
| ERD | `diagrams/erd.mmd` | Database entity relationships |
| Recommendation State | `diagrams/recommendation-state.mmd` | Recommendation lifecycle state machine |
| Data Lineage | `diagrams/data-lineage.mmd` | Data flow from raw to presentation |

## Appendix C: Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/vinemind

# Authentication
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# External APIs
OPENWEATHER_API_KEY=your_key
MAPBOX_ACCESS_TOKEN=pk.eyJ...

# AI Copilot
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_key

# Application
NODE_ENV=development
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# Geospatial Data
DATA_DIR=./data/et-geo
RASTER_CACHE_DIR=./cache/rasters
```

## Appendix D: Development Setup

```bash
# Prerequisites
docker --version        # 24+
docker compose --version # 2+
node --version           # 20+
python --version         # 3.11+

# Quick Start
git clone https://github.com/vinemind/vinemind-ai.git
cd vinemind-ai
cp .env.example .env
docker compose up -d

# Access
Frontend:     http://localhost:3000
API:          http://localhost:8000
API Docs:     http://localhost:8000/docs
Database:     localhost:5432
```
