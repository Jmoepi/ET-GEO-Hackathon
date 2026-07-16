# VineMind AI
# Frontend Architecture Specification

---

| Property | Value |
|----------|-------|
| Document ID | VM-010 |
| Version | 1.0 |
| Status | Draft |
| Standard | Frontend Architecture Specification |
| Project | VineMind AI |
| Author | Jeffrey Moepi |
| Last Updated | 16 July 2026 |
| Related Documents | VM-003 System Architecture, VM-006 Decision Intelligence Engine, VM-008 API Specification |

---

# Table of Contents

1. Introduction
2. Frontend Philosophy
3. Design Principles
4. Technology Stack
5. High-Level Architecture
6. Application Structure
7. Navigation Architecture
8. Core Pages
9. Component Architecture
10. State Management
11. Mapping & Geospatial Visualisation
12. Explainable Decision Experience
13. AI Copilot Experience
14. Design System
15. Responsive Design
16. Performance
17. Accessibility
18. Future Evolution

---

# 1. Introduction

The VineMind frontend provides an intuitive Decision Intelligence Workspace that enables vineyard managers to monitor vineyard health, understand irrigation recommendations, investigate water stress, and interact with the Explainable AI Copilot.

Unlike traditional dashboards that display disconnected charts and maps, VineMind is designed around decision support. Every screen exists to help users answer three questions:

- What is happening?
- Why is it happening?
- What should I do next?

The frontend never performs scientific calculations. It visualises and explains outputs produced by the Decision Intelligence Engine.

---

# 2. Frontend Philosophy

The frontend follows four core principles.

## Decision First

The most important information is always the recommended action.

---

## Explain Before Display

Recommendations are accompanied by evidence and confidence.

---

## Progressive Disclosure

Users see summaries first and can progressively explore supporting detail.

---

## Geospatial Native

Maps are the primary navigation experience rather than an optional feature.

---

# 3. Design Principles

The interface should be:

- Clean
- Fast
- Minimal
- Mobile friendly
- Accessible
- Explainable
- Data-driven

Every component should reduce cognitive load rather than increase it.

---

# 4. Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | React 19 |
| Language | TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Maps | Mapbox GL JS |
| Charts | Recharts |
| Icons | Lucide React |
| State Management | TanStack Query + Zustand |
| Forms | React Hook Form |
| Routing | React Router |

---

# 5. High-Level Architecture

```text
React Application
│
├── Authentication
├── Dashboard
├── Vineyard Explorer
├── Map Workspace
├── Decision Centre
├── Analytics
├── Reports
├── AI Copilot
└── Settings
```

The frontend communicates exclusively through the REST API.

No direct database access exists.

---

# 6. Application Structure

```text
src/

├── app/
├── pages/
├── layouts/
├── components/
│
├── map/
├── charts/
├── cards/
├── tables/
├── copilot/
├── alerts/
│
├── hooks/
├── services/
├── api/
├── state/
├── utils/
├── styles/
└── assets/
```

Each module has a single responsibility.

---

# 7. Navigation Architecture

```text
Dashboard

↓

Vineyard Explorer

↓

Block Details

↓

Decision Analysis

↓

Decision Evidence

↓

Historical Trends
```

Users drill deeper into information instead of navigating between disconnected screens.

---

# 8. Core Pages

## Dashboard

Provides a high-level operational overview.

Displays:

- Total vineyard health
- Water Stress Summary
- Irrigation priorities
- Weather overview
- Active alerts

---

## Vineyard Explorer

Interactive map showing:

- Vineyard boundaries
- Block status
- Water Stress colours
- Recommendation overlays

---

## Block Details

Displays:

- ETa
- ETo
- NDVI
- Soil moisture
- Weather
- Water Stress Score
- Recommendation
- Decision Evidence

---

## Decision Centre

A workspace showing:

- Irrigation priorities
- Confidence
- Supporting evidence
- Historical decisions

---

## Analytics

Provides historical analysis including:

- Water usage trends
- Stress trends
- NDVI evolution
- Seasonal comparisons

---

## Reports

Generate downloadable PDF reports.

---

## AI Copilot

Provides a conversational interface for exploring vineyard intelligence.

The Copilot explains decisions but never creates recommendations.

---

# 9. Component Architecture

Reusable components include:

```text
Button

Card

Map

Metric Card

Chart Card

Recommendation Card

Confidence Badge

Evidence Timeline

Alert Banner

Data Table

Copilot Panel
```

Each component is designed for composability and reuse.

---

# 10. State Management

The frontend separates state into three categories.

## Server State

Managed using TanStack Query.

Examples:

- Recommendations
- Vineyard data
- Weather
- Reports

---

## UI State

Managed using Zustand.

Examples:

- Sidebar
- Selected vineyard
- Theme
- Map settings

---

## Form State

Managed using React Hook Form.

---

# 11. Mapping & Geospatial Visualisation

Maps are central to the user experience.

Capabilities include:

- Vineyard polygons
- Block boundaries
- Colour-coded Water Stress
- Satellite imagery
- Recommendation overlays
- Layer switching
- Block selection
- Hover insights

Spatial interactions update the surrounding analytics automatically.

---

# 12. Explainable Decision Experience

Every recommendation displays:

- Recommendation
- Priority
- Confidence
- Water Stress Score
- Evidence
- Timestamp
- Model Version

Users can expand each recommendation to inspect the complete Decision Evidence Package.

---

# 13. AI Copilot Experience

The AI Copilot is presented as an Explainable Intelligence Assistant.

Example questions include:

- Why is Block A12 stressed?
- Which block should I irrigate first?
- Compare today with yesterday.
- Explain today's recommendations.
- Summarise vineyard health.

Every response references the Decision Evidence Package rather than generating unsupported advice.

---

# 14. Design System

Colours communicate operational meaning.

| Colour | Meaning |
|---------|---------|
| Green | Healthy |
| Blue | Adequate Water |
| Yellow | Monitor |
| Orange | High Stress |
| Red | Critical |
| Grey | Missing Data |

Typography prioritises readability.

Spacing follows an 8-point grid.

Cards use consistent elevation and border radii.

---

# 15. Responsive Design

Supported breakpoints include:

| Device | Width |
|---------|-------|
| Mobile | <640 px |
| Tablet | 640–1024 px |
| Desktop | >1024 px |

The map becomes full-screen on smaller devices with collapsible analytical panels.

---

# 16. Performance

Performance goals:

| Metric | Target |
|---------|--------|
| Initial Load | <2 s |
| Map Render | <1 s |
| API Updates | <300 ms |
| Lighthouse Score | >95 |

Performance optimisation includes:

- Lazy loading
- Route splitting
- Image optimisation
- API caching
- Virtualised tables

---

# 17. Accessibility

The application follows WCAG 2.2 AA guidelines.

Features include:

- Keyboard navigation
- Screen reader compatibility
- High contrast support
- Focus indicators
- Semantic HTML
- Accessible colour combinations

---

# 18. Future Evolution

Future enhancements may include:

- Native mobile application
- Offline field mode
- Voice-enabled AI Copilot
- Augmented reality vineyard overlays
- Drone imagery playback
- Multi-farm management
- Live IoT dashboards
- Collaborative decision reviews

---

# Appendix A
## Frontend Interaction Flow

```text
User

↓

Dashboard

↓

Select Vineyard

↓

Map Highlights Block

↓

View Recommendation

↓

Inspect Decision Evidence

↓

Ask AI Copilot

↓

Generate Report
```

---

# Appendix B
## Frontend Layering

```text
Presentation Layer

↓

UI Components

↓

Feature Modules

↓

State Management

↓

API Services

↓

REST API
```

---

# Conclusion

The VineMind frontend is designed as a Decision Intelligence Workspace that transforms complex geospatial and environmental data into actionable operational insight. By combining interactive mapping, explainable recommendations, and a conversational AI interface, the application enables vineyard managers to understand not only what action is recommended but also the evidence behind every recommendation. The architecture emphasises usability, transparency, scalability, and maintainability, providing a strong foundation for both the ET-GEO Hackathon prototype and future production deployment.