# VineMind AI

**Intelligent Vineyard Irrigation Decision-Support Platform**

VineMind AI converts TerraClim ET-GEO evapotranspiration data into clear, explainable, prioritised irrigation recommendations for vineyard managers. Rather than a traditional GIS dashboard, it acts as a digital agronomic assistant — interpreting satellite observations, environmental conditions, and vineyard characteristics to recommend practical irrigation actions at the vineyard-block level.

**Hackathon:** TerraClim ET-GEO Hackathon 2026
**Author:** Jeffrey Moepi

---

## Core Problem

Current irrigation workflows are data-driven rather than decision-driven. Datasets (ETa, ETo, Kc, NDVI, soil moisture, phenology, weather) rarely answer the operational question: *"Which vineyard blocks should I irrigate today, how much water, and why?"*

## Core Innovation

A **deterministic Water Stress Model** that produces reproducible, fully explainable scores, paired with an **Explainable AI Copilot** that interprets recommendations without ever generating incorrect advice.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, Recharts |
| Mapping | Mapbox GL JS, react-map-gl |
| State | TanStack Query (server), Zustand (UI) |
| Backend | FastAPI (Python 3.11+) |
| Database | PostgreSQL 16 + PostGIS |
| ORM | SQLAlchemy (async) |
| Geospatial | Rasterio, GeoPandas, Shapely, NumPy |
| AI/LLM | Azure OpenAI (read-only Copilot) |
| Auth | JWT + Argon2id password hashing |
| Containerisation | Docker Compose |

---

## Project Structure

```
vine-mind-ai/
├── docs/                          # 24 technical documentation files
│   ├── 00-Executive-Summary.md
│   ├── 07-Water-Stress-Model.md   # WSM-1.0 specification
│   ├── 08-API-Specification.md
│   ├── 09-Database-Design.md
│   ├── 18-Design-System.md
│   ├── 19-UX-Flows-Wireframes.md
│   ├── VineMind-Technical-Blueprint.md
│   └── diagrams/                  # 18 Mermaid architecture diagrams
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── config.py              # Pydantic settings
│   │   ├── database.py            # Async SQLAlchemy engine
│   │   ├── core/                  # Security, auth dependencies
│   │   ├── models/                # 7 SQLAlchemy models
│   │   ├── schemas/               # Pydantic request/response
│   │   ├── services/              # CRUD service layer
│   │   ├── decision_engine/       # Water Stress Model + DEP generation
│   │   ├── geospatial/            # Raster/vector processing
│   │   └── api/v1/                # REST endpoint handlers
│   ├── seed.py                    # Demo data seeder
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                   # Routing + app shell
│   │   ├── pages/                 # Dashboard, Explorer, Decision Centre, Copilot
│   │   ├── components/ui/         # StressBadge, MetricCard, etc.
│   │   ├── hooks/                 # TanStack Query hooks
│   │   ├── services/              # API client
│   │   ├── state/                 # Zustand stores
│   │   └── utils/                 # Types + helpers
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### One-Command Setup

```bash
cp .env.example .env
docker compose up -d
cd backend && python -m seed
```

This starts PostgreSQL + PostGIS, the FastAPI backend, and builds the frontend.

### Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Database | localhost:5432 |

### Demo Login

```
Email:    jeffrey@vinemind.ai
Password: demo1234
```

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m seed              # Create tables + seed demo data
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                 # Vite dev server on :3000, proxies /api to :8000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Authenticate (returns JWT) |
| POST | `/api/v1/auth/register` | Create account |
| GET | `/api/v1/auth/me` | Current user profile |
| GET | `/api/v1/vineyards` | List vineyards |
| GET | `/api/v1/blocks` | List blocks |
| GET | `/api/v1/stress/{blockId}` | Current water stress score |
| GET | `/api/v1/stress/history/{blockId}` | Historical stress scores |
| POST | `/api/v1/stress/calculate/{blockId}` | Trigger stress calculation |
| GET | `/api/v1/recommendations` | List recommendations |
| GET | `/api/v1/recommendations/{blockId}` | Block recommendation |
| GET | `/api/v1/evidence/{blockId}` | Decision Evidence Package |
| POST | `/api/v1/copilot/chat` | AI Copilot (read-only) |

---

## Water Stress Model (WSM-1.0)

A deterministic weighted linear model. Identical inputs always produce identical outputs.

| Feature | Weight | Description |
|---------|--------|-------------|
| Water Deficit | 30% | ETo − ETa |
| ET Ratio | 20% | ETa / ETo |
| Soil Moisture Index | 20% | Current / Seasonal Average |
| NDVI Trend | 15% | Current NDVI − Previous NDVI |
| Rainfall Offset | 10% | Forecast Rain − Irrigation Requirement |
| Phenology Weight | 5% | Growth stage sensitivity multiplier |

### Stress Categories

| Score | Category | Action |
|-------|----------|--------|
| 0–20 | Healthy | No Action Required |
| 21–40 | Monitor | Monitor Tomorrow |
| 41–60 | Moderate | Delay Irrigation |
| 61–80 | High Stress | Irrigate Tonight |
| 81–100 | Critical | Irrigate Immediately |

Every recommendation produces a **Decision Evidence Package (DEP)** — a structured JSON audit trail with all input data, feature weights, normalised scores, confidence, model version, and rules triggered.

---

## Documentation

| Document | File |
|----------|------|
| Executive Summary | `docs/00-Executive-Summary.md` |
| Product Vision | `docs/01-Product-Vision.md` |
| Requirements | `docs/02-Requirements-Specification.md` |
| System Architecture | `docs/03-System-Architecture.md` |
| Data Architecture | `docs/04-Data-Architecture.md` |
| Geospatial Pipeline | `docs/05-Geospatial-Pipeline.md` |
| Decision Engine | `docs/06-Recommendation-Engine.md` |
| Water Stress Model | `docs/07-Water-Stress-Model.md` |
| AI Copilot | `docs/07-AI-Copilot-Architecture.md` |
| API Specification | `docs/08-API-Specification.md` |
| Database Design | `docs/09-Database-Design.md` |
| Frontend Architecture | `docs/10-Frontend-Architecture.md` |
| Backend Architecture | `docs/11-Backend-Architecture.md` |
| Deployment Guide | `docs/12-Deployment-Guide.md` |
| Testing Strategy | `docs/13-Testing-Strategy.md` |
| Development Roadmap | `docs/14-Development-Roadmap.md` |
| AI Governance | `docs/15-AI-Governance-Explainability.md` |
| Operations | `docs/16-Operations-Monitoring.md` |
| ADRs | `docs/17-Architecture-Decision-Records.md` |
| Design System | `docs/18-Design-System.md` |
| UX Flows | `docs/19-UX-Flows-Wireframes.md` |
| Technical Blueprint | `docs/VineMind-Technical-Blueprint.md` |

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://vinemind:vinemind@localhost:5432/vinemind

# Authentication
JWT_SECRET=your-secret-key

# External APIs
OPENWEATHER_API_KEY=your_key
MAPBOX_ACCESS_TOKEN=pk.your_token

# AI Copilot
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_key
```

---

## License

Built for the TerraClim ET-GEO Hackathon 2026.
