

---

# 17. Architecture Decision Records (ADR)

## 17.1 Introduction

Architecture Decision Records (ADRs) document the significant architectural choices made during VineMind AI's development, the context in which they were made, and their consequences. Each ADR follows a consistent format and is immutable once accepted — future changes create new ADRs that reference the original.

## 17.2 ADR Format

Each ADR follows this template:

```
# ADR-[NNN]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
What is the issue that motivates this decision?

## Decision
What is the change being proposed?

## Consequences
What are the positive and negative outcomes?

## Alternatives Considered
What other options were evaluated?
```

---

## ADR-001: FastAPI as Backend Framework

**Status:** Accepted

### Context

VineMind AI requires a Python backend that can:
- Serve a REST API with OpenAPI documentation
- Handle async I/O for database and external API calls
- Integrate with the scientific Python ecosystem (Rasterio, GeoPandas, NumPy)
- Support rapid development during a hackathon timeline
- Perform well under moderate load

### Decision

Use **FastAPI** (Python 3.11+) as the primary backend web framework.

### Consequences

**Positive:**
- Native async support for concurrent database and API calls
- Automatic OpenAPI/Swagger documentation generation
- Pydantic integration for request/response validation
- Performance comparable to Node.js for I/O-bound workloads
- Excellent integration with scientific Python libraries
- Strong type hints improve code reliability and IDE support

**Negative:**
- Smaller ecosystem than Django for admin/ORM features
- Less mature than Flask for certain edge cases
- Team needs to learn Pydantic patterns

### Alternatives Considered

| Framework | Pros | Cons | Decision |
|-----------|------|------|----------|
| **Django REST Framework** | Mature, full-featured, admin UI | Heavier, slower async, ORM overhead | Rejected — too heavy for API-only service |
| **Flask** | Lightweight, simple, large ecosystem | No native async, no automatic docs | Rejected — lacks modern features |
| **FastAPI** | Async, auto-docs, Pydantic, fast | Smaller ecosystem, newer | **Accepted** |

---

## ADR-002: PostgreSQL + PostGIS as Primary Database

**Status:** Accepted

### Context

VineMind AI stores:
- Vineyard block boundaries (polygons)
- Spatial queries (which blocks are in a region?)
- Time-series observations (daily ETa, ETo, NDVI)
- Recommendation history
- User accounts and audit logs

The database must handle both geospatial and relational data efficiently.

### Decision

Use **PostgreSQL 16 with PostGIS extension** as the primary database.

### Consequences

**Positive:**
- PostGIS provides industry-standard geospatial capabilities (ST_Within, ST_Area, ST_Intersects)
- Mature, battle-tested database with excellent reliability
- Strong ACID compliance for data integrity
- pg_dump for straightforward backup
- PostGIS GiST indexes for fast spatial queries
- Single database handles both relational and geospatial data

**Negative:**
- PostGIS learning curve for complex spatial queries
- Horizontal scaling requires more effort than NoSQL
- Geospatial indexing requires careful schema design

### Alternatives Considered

| Database | Pros | Cons | Decision |
|----------|------|------|----------|
| **PostgreSQL + PostGIS** | Spatial + relational, mature, reliable | Horizontal scaling complexity | **Accepted** |
| **MongoDB + GeoJSON** | Flexible schema, horizontal scaling | Weaker consistency, no PostGIS depth | Rejected — insufficient spatial maturity |
| **TimescaleDB** | Excellent time-series | Less mature spatial features | Rejected for MVP; considered for future |
| **Supabase** | Managed PostGIS, auth built-in | Vendor dependency, less control | Rejected — preference for self-managed |

---

## ADR-003: React + TypeScript for Frontend

**Status:** Accepted

### Context

The frontend must:
- Display interactive maps with vineyard boundaries
- Show real-time recommendation data
- Be responsive for desktop and tablet use
- Be buildable within a hackathon timeline
- Support future mobile adaptation

### Decision

Use **React 19 with TypeScript** as the frontend framework, with:
- Vite as the build tool
- Tailwind CSS + shadcn/ui for styling
- Mapbox GL JS for interactive mapping
- Recharts for data visualisation
- TanStack Query for server state management
- Zustand for UI state management

### Consequences

**Positive:**
- TypeScript catches errors at compile time
- Large ecosystem of libraries and community support
- Vite provides fast development and build times
- React Native can be used for future mobile app with shared logic
- Component-based architecture matches design system approach

**Negative:**
- React ecosystem has many choices (decision fatigue)
- Mapbox GL JS requires API key and has usage costs
- SSR not needed for this application (Vercel handles well)

### Alternatives Considered

| Framework | Pros | Cons | Decision |
|-----------|------|------|----------|
| **Next.js** | SSR, full-stack, Vercel-native | SSR overhead not needed, heavier | Rejected — SPA sufficient |
| **Vue 3** | Simpler API, good DX | Smaller ecosystem, fewer mapping libs | Rejected — React ecosystem advantage |
| **Svelte** | Smallest bundle, fastest runtime | Smaller ecosystem, less mapping support | Rejected — ecosystem maturity |
| **React + Vite** | Fast, flexible, large ecosystem | More manual setup than Next.js | **Accepted** |

---

## ADR-004: Deterministic Water Stress Model (Rule-Based First)

**Status:** Accepted

### Context

The core innovation is converting ET-GEO datasets into actionable irrigation recommendations. The model must:
- Be explainable (every recommendation must show why)
- Be reproducible (same inputs → same outputs)
- Work with limited training data (hackathon scope)
- Be trusted by vineyard managers (no black boxes)
- Be upgradeable to ML in future phases

### Decision

Implement a **deterministic weighted linear model** (Water Stress Model v1.0) with configurable feature weights, rather than starting with machine learning.

```
Stress Score = Σ(Normalised_Feature × Weight) × 100
```

Features: Water Deficit (30%), ET Ratio (20%), Soil Moisture (20%), NDVI Trend (15%), Rain Forecast (10%), Phenology Weight (5%).

### Consequences

**Positive:**
- 100% explainable — every score traces back to input features and weights
- Reproducible — identical inputs always produce identical outputs
- No training data required — works immediately with ET-GEO data
- Fast to implement and validate during hackathon
- Clear upgrade path to ML models (WSM-2.0, WSM-3.0)
- Agronomists can understand and validate the logic

**Negative:**
- Weights are manually tuned (may not be optimal)
- Linear model may miss non-linear interactions between features
- Less adaptive than ML models to new patterns

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **Weighted Linear** | Simple, explainable, deterministic | May miss non-linear patterns | **Accepted for MVP** |
| **Decision Tree** | Somewhat explainable | Requires training data | Rejected — insufficient data |
| **Random Forest** | High accuracy | Black box, needs training data | Rejected — not for MVP |
| **Neural Network** | Highest potential accuracy | Completely opaque, needs data | Rejected — not for MVP |

---

## ADR-005: Decision Evidence Package (DEP) as Explainability Standard

**Status:** Accepted

### Context

Every recommendation must be explainable and auditable. The AI Copilot, Dashboard, and Reports all need to present consistent explanations. There must be a single source of truth for why a recommendation was made.

### Decision

Implement a **Decision Evidence Package (DEP)** — a structured JSON object stored with every recommendation containing all input data, model outputs, decision rules, and confidence metrics.

```json
{
  "recommendation_id": "rec_001",
  "block_id": "blk_abc",
  "stress_score": 74,
  "confidence": 0.87,
  "contributors": [
    {"metric": "water_deficit", "value": 4.2, "unit": "mm", "weight": 0.30},
    {"metric": "et_ratio", "value": 0.82, "unit": "ratio", "weight": 0.20},
    {"metric": "ndvi_trend", "value": -0.08, "unit": "ndvi", "weight": 0.15}
  ],
  "decision_rules_triggered": ["rule_high_stress_no_rain"],
  "model_version": "WSM-1.0"
}
```

### Consequences

**Positive:**
- Every recommendation is fully auditable months or years later
- AI Copilot can reference the DEP to explain decisions
- Dashboard can visualise evidence in a structured way
- Reports can include complete evidence trails
- New team members can understand historical decisions
- Debugging recommendation quality is straightforward

**Negative:**
- Increased storage per recommendation (~2-5KB per DEP)
- Requires careful schema evolution as model improves
- Adds complexity to recommendation generation pipeline

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **Decision Evidence Package** | Complete auditability, single source of truth | Storage overhead, schema complexity | **Accepted** |
| **Separate audit log** | Simpler storage | Not tied to recommendations, harder to query | Rejected |
| **Narrative text only** | Human-readable | Not machine-parseable, inconsistent | Rejected |
| **No evidence** | Simplest | Unexplainable, untrustworthy | Rejected |

---

## ADR-006: Explainable AI Copilot (Never Decides)

**Status:** Accepted

### Context

Users want to interact with the platform using natural language. However, allowing an LLM to generate irrigation recommendations would undermine the deterministic, auditable nature of the Water Stress Model and Decision Intelligence Engine.

### Decision

The AI Copilot is a **read-only explanation layer** that:
- Explains existing recommendations (never creates new ones)
- Compares blocks using data from the DEP
- Summarises trends from historical data
- Generates natural-language reports
- Always cites its evidence and confidence
- Never overrides or modifies the Decision Intelligence Engine

### Consequences

**Positive:**
- LLM cannot produce incorrect irrigation advice
- Deterministic decision engine remains the single source of truth
- Users trust recommendations because they come from the model, not AI
- Clear separation of concerns (science vs. communication)
- Hallucination risk is contained to explanations, not decisions

**Negative:**
- Copilot cannot answer "what if" questions about irrigation
- Less interactive than a full conversational AI
- Requires maintaining the boundary between explanation and decision

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **Read-Only Copilot** | Safe, auditable, deterministic decisions | Less interactive | **Accepted** |
| **Full Conversational AI** | More interactive, can suggest actions | Risk of incorrect advice, opaque | Rejected — safety concern |
| **No AI** | Simplest, no risk | Poor user experience | Rejected |
| **Copilot with approval** | Can suggest, human approves | Increases cognitive load | Deferred to Phase 3 |

---

## ADR-007: Docker-First Deployment

**Status:** Accepted

### Context

The platform must run consistently across development, hackathon demo, and production environments. Multiple team members need to develop locally. The hackathon judges need a reliable demo.

### Decision

Use **Docker Compose** for local development and demo, with Docker images deployed to managed platforms (Vercel for frontend, Railway/Render for backend, managed PostgreSQL).

### Consequences

**Positive:**
- "Works on my machine" eliminated — same container everywhere
- Simple `docker compose up` for instant local setup
- Hackathon demo is reliable and reproducible
- Easy to containerise new services as architecture evolves
- GitHub Actions builds Docker images for CI/CD

**Negative:**
- Docker adds complexity for developers unfamiliar with containers
- Image sizes can be large with geospatial libraries (GDAL, GEOS)
- Docker Compose networking differs slightly from Kubernetes

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **Docker Compose** | Consistent, simple, portable | Slightly heavier than bare metal | **Accepted** |
| **Vagrant** | Full VM control | Heavier, slower, more complex | Rejected |
| **Bare metal** | Fastest, simplest | Environment drift, "works on my machine" | Rejected |
| **Kubernetes** | Production-grade orchestration | Overkill for hackathon, steep learning curve | Deferred to Phase 3 |

---

## ADR-008: Append-Only Historical Data

**Status:** Accepted

### Context

Irrigation decisions must be auditable over time. Historical observations must never be overwritten because:
- Past recommendations must remain explainable
- Trends require consistent historical data
- Regulatory compliance may require data retention

### Decision

All observation and recommendation data is **append-only**. New data creates new records; updates create new versions rather than modifying existing rows.

### Consequences

**Positive:**
- Complete audit trail of all data over time
- Historical recommendations remain accurate (they reference original observations)
- Trend analysis is reliable — no data loss from updates
- Compliance-ready for water usage reporting

**Negative:**
- Storage grows faster than mutable approach
- Queries must always filter to "latest" version
- Data cleanup requires explicit archival policies

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **Append-only** | Complete history, audit trail, reliable trends | Higher storage, query complexity | **Accepted** |
| **Mutable with versioning** | Lower storage, simpler queries | Risk of breaking historical recommendations | Rejected |
| **Mutable (latest only)** | Simplest | Loses history, breaks auditing | Rejected |

---

## ADR-009: REST API with URI Versioning

**Status:** Accepted

### Context

The API must serve the React dashboard, future mobile apps, and potential third-party integrations. It must evolve without breaking existing clients.

### Decision

Use **URI-based versioning** (`/api/v1/...`) with a well-defined API contract documented via OpenAPI 3.0. Older versions supported during migration periods.

### Consequences

**Positive:**
- Clear version boundaries for breaking changes
- OpenAPI docs generated automatically from FastAPI
- Client code can migrate at its own pace
- API contract is explicit and testable

**Negative:**
- URI versioning can lead to code duplication
- Need to maintain multiple versions during migration
- Header-based versioning is technically "cleaner" but harder to test

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **URI versioning** (/api/v1/) | Simple, explicit, cacheable | Code duplication | **Accepted** |
| **Header versioning** | Clean URIs, no duplication | Harder to test, less visible | Rejected |
| **Query parameter** | Simple | Cache-unfriendly, less standard | Rejected |
| **No versioning** | Simplest | Breaks clients on changes | Rejected |

---

## ADR-010: Mapbox GL JS for Mapping

**Status:** Accepted

### Context

The platform requires an interactive map that can:
- Display vineyard block boundaries (polygons)
- Overlay colour-coded stress indicators
- Support zoom, pan, and block selection
- Perform well with many polygons
- Be easy to integrate with React

### Decision

Use **Mapbox GL JS** for interactive mapping, with Mapbox-hosted vector tiles and satellite imagery basemap.

### Consequences

**Positive:**
- High-performance vector tile rendering (WebGL)
- Satellite imagery basemap shows actual vineyard conditions
- Rich styling API for stress colour overlays
- Strong React integration via `react-map-gl`
- Free tier sufficient for hackathon and early development

**Negative:**
- Requires Mapbox API key and account
- Free tier has usage limits
- Proprietary (not fully open source)
- Styling syntax has a learning curve

### Alternatives Considered

| Library | Pros | Cons | Decision |
|---------|------|------|----------|
| **Mapbox GL JS** | High performance, satellite imagery, React support | Proprietary, usage limits | **Accepted** |
| **MapLibre GL JS** | Fully open source, Mapbox fork | Less polished documentation | Rejected — Mapbox ecosystem more mature |
| **Leaflet** | Simple, lightweight | Raster-only, poor performance with many polygons | Rejected — insufficient for vector data |
| **OpenLayers** | Very powerful, full-featured | Steep learning curve, heavier bundle | Rejected — overkill for this use case |

---

## Summary of Decisions

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 | FastAPI | Async Python, auto-docs, scientific ecosystem |
| ADR-002 | PostgreSQL + PostGIS | Spatial + relational, mature, reliable |
| ADR-003 | React + TypeScript | Ecosystem, type safety, mapping support |
| ADR-004 | Deterministic Weighted Model | Explainable, reproducible, no training data needed |
| ADR-005 | Decision Evidence Package | Auditability, single source of truth for explanations |
| ADR-006 | Read-Only AI Copilot | Safety, deterministic decisions, trust |
| ADR-007 | Docker Compose | Consistent environments, simple demo |
| ADR-008 | Append-Only Data | Audit trail, reliable historical analysis |
| ADR-009 | URI Versioning | Clear API evolution, explicit contract |
| ADR-010 | Mapbox GL JS | High performance, satellite imagery, React support |
