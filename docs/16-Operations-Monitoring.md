

---

# 16. Operations & Monitoring Specification

## 16.1 Introduction

This document defines the observability, logging, metrics, alerting, and incident management strategy for VineMind AI. It ensures the platform is reliable, debuggable, and operationally mature from day one of the hackathon MVP.

## 16.2 Operational Principles

| Principle | Description |
|-----------|-------------|
| **Observability by Default** | Every service emits structured logs, metrics, and traces from the first line of code |
| **Alert on Symptoms** | Alert on user-visible impact (latency, errors), not internal implementation details |
| **Fail Loudly** | Errors must be visible and actionable, never silently swallowed |
| **Single Pane of Glass** | One dashboard provides the full operational picture |
| **Automate Toil** | Any manual operational task repeated more than twice gets automated |

## 16.3 Observability Stack

### 16.3.1 Three Pillars

```
┌──────────────────────────────────────────────────────────┐
│                  OBSERVABILITY STACK                       │
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   LOGS      │  │   METRICS   │  │   TRACES    │      │
│  │             │  │             │  │             │      │
│  │ Structured  │  │ Prometheus  │  │ OpenTelemetry│     │
│  │ JSON output │  │ + Grafana   │  │ (Future)    │      │
│  │             │  │             │  │             │      │
│  │ Who, What,  │  │ Rate, Error,│  │ Request     │      │
│  │ When        │  │ Duration    │  │ Flow        │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                           │
│  ┌───────────────────────────────────────────────────┐   │
│  │              ALERTING & NOTIFICATION               │   │
│  │  Grafana Alerts → Email / Slack / Webhook          │   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### 16.3.2 Technology Choices

| Pillar | Technology | Purpose | MVP |
|--------|------------|---------|-----|
| Logs | Python `structlog` | Structured JSON logs | Yes |
| Log Aggregation | File-based (future: ELK) | Centralised log storage | Partial |
| Metrics | Prometheus (future) | Time-series metrics | No (future) |
| Dashboards | Grafana (future) | Operational dashboards | No (future) |
| Traces | OpenTelemetry (future) | Distributed tracing | No (future) |
| Alerting | Grafana Alerts (future) | Threshold-based alerts | No (future) |

**MVP Approach:** Structured logging to stdout/stderr, consumed by platform log drain (Railway/Vercel). Simple health check endpoints.

## 16.4 Logging Strategy

### 16.4.1 Structured Log Format

```json
{
  "timestamp": "2026-07-16T08:30:00Z",
  "level": "INFO",
  "service": "decision-engine",
  "message": "Recommendation generated",
  "block_id": "blk_abc123",
  "stress_score": 74,
  "recommendation": "irrigate_tonight",
  "confidence": 0.87,
  "model_version": "WSM-1.0",
  "request_id": "req_xyz789",
  "user_id": "usr_001",
  "duration_ms": 142
}
```

### 16.4.2 Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| `DEBUG` | Detailed diagnostic info (dev only) | Feature normalisation values, raster pixel counts |
| `INFO` | Normal operations | Recommendation generated, data ingested, user logged in |
| `WARNING` | Degraded but recoverable | Weather API fallback to cache, missing NDVI used previous |
| `ERROR` | Operation failed, user impact | Database connection failed, raster processing error |
| `CRITICAL` | System-level failure | Data corruption detected, recommendation engine offline |

### 16.4.3 Events to Log

| Event Category | Events | Level |
|----------------|--------|-------|
| **Lifecycle** | Service start, shutdown, migration run | INFO |
| **Authentication** | Login success, login failure, token refresh, logout | INFO / WARNING |
| **Data Ingestion** | GeoTIFF loaded, polygon imported, ingestion failed | INFO / ERROR |
| **Recommendation** | Score calculated, recommendation generated, DEP created | INFO |
| **AI Copilot** | User query, intent detected, response generated | INFO |
| **API Requests** | Request received (with request_id) | DEBUG |
| **Errors** | Exception raised, database error, external API failure | ERROR |
| **Security** | Unauthorised access attempt, rate limit exceeded | WARNING |
| **Performance** | Slow query detected, processing duration | WARNING |

### 16.4.4 Log Sanitisation

The following fields are **never** logged:
- Passwords or password hashes
- JWT tokens
- API keys
- Personal identifiable information beyond user ID
- Database connection strings

## 16.5 Health Checks

### 16.5.1 Endpoints

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `GET /health` | GET | Service alive | `200 OK` with status |
| `GET /health/ready` | GET | Ready to accept traffic | `200 OK` or `503` |
| `GET /health/live` | GET | Liveness probe | `200 OK` or `503` |

### 16.5.2 Health Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "checks": {
    "database": "ok",
    "geospatial_pipeline": "ok",
    "recommendation_engine": "ok",
    "ai_copilot": "degraded"
  },
  "last_recommendation_run": "2026-07-16T06:00:00Z"
}
```

### 16.5.3 Readiness Checks

The `/ready` endpoint verifies:
- Database connection is active and responsive
- Recent data ingestion has occurred (within last 48 hours)
- Recommendation engine can process requests
- Required external APIs are reachable

## 16.6 Metrics

### 16.6.1 Application Metrics

| Metric | Type | Description | Target |
|--------|------|-------------|--------|
| `api_requests_total` | Counter | Total API requests by endpoint and status | — |
| `api_request_duration_seconds` | Histogram | Request latency distribution | p95 < 800ms |
| `recommendations_generated_total` | Counter | Daily recommendations generated | — |
| `water_stress_score_distribution` | Histogram | Distribution of stress scores | — |
| `ai_copilot_requests_total` | Counter | Copilot requests by intent | — |
| `ai_copilot_latency_seconds` | Histogram | Copilot response time | p95 < 3s |
| `geospatial_processing_duration_seconds` | Histogram | Raster processing time | < 30s per batch |
| `data_ingestion_events_total` | Counter | Data ingestion by source | — |
| `active_users_gauge` | Gauge | Currently active sessions | — |

### 16.6.2 Infrastructure Metrics

| Metric | Type | Description | Target |
|--------|------|-------------|--------|
| `process_cpu_seconds_total` | Counter | CPU usage | — |
| `process_resident_memory_bytes` | Gauge | Memory usage | < 512MB |
| `db_connections_active` | Gauge | Database connections | < 20 |
| `db_query_duration_seconds` | Histogram | Database query latency | p95 < 100ms |

### 16.6.3 Agricultural Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `blocks_irrigated_today` | Gauge | Number of blocks recommended for irrigation |
| `total_water_deficit_mm` | Gauge | Sum of water deficits across all blocks |
| `average_stress_score` | Gauge | Mean stress score across all blocks |
| `critical_stress_blocks` | Gauge | Blocks with stress score > 80 |

## 16.7 Alerting

### 16.7.1 Alert Severity Levels

| Level | Description | Response Time | Notification |
|-------|-------------|---------------|--------------|
| **P0 — Critical** | System down, data loss risk | Immediate | Email + Slack + SMS |
| **P1 — High** | Feature degraded, user impact | < 30 minutes | Email + Slack |
| **P2 — Medium** | Degraded performance, workaround exists | < 4 hours | Email |
| **P3 — Low** | Minor issue, no user impact | Next business day | Log only |

### 16.7.2 Alert Rules

| Alert | Condition | Severity | Message |
|-------|-----------|----------|---------|
| Service Down | Health check fails 3x | P0 | "VineMind AI service is unresponsive" |
| Database Unreachable | Connection pool exhausted | P0 | "PostgreSQL connection pool exhausted" |
| High Error Rate | 5xx > 5% for 5 minutes | P1 | "Elevated error rate: {rate}%" |
| Slow API Responses | p95 > 2s for 10 minutes | P1 | "API latency above threshold" |
| Data Stale | No ingestion > 48 hours | P1 | "Geospatial data is stale — last update {time}" |
| Recommendation Engine Fail | Processing errors > 10% | P1 | "Recommendation engine degraded" |
| AI Copilot Errors | Error rate > 20% | P2 | "AI Copilot experiencing errors" |
| Memory High | Usage > 80% | P2 | "Memory usage at {percent}%" |
| Disk Space Low | < 20% remaining | P2 | "Disk space low: {available}GB remaining" |
| Slow Queries | Query > 5s | P3 | "Slow query detected: {query}" |

### 16.7.3 Alert Routing

```
P0/P1 Alerts → Email (jeffrey@vinemind.ai) + Slack #vinemind-alerts
P2 Alerts    → Email (jeffrey@vinemind.ai)
P3 Alerts    → Logged only (reviewed during standup)
```

## 16.8 Incident Management

### 16.8.1 Incident Lifecycle

```
Detection → Triage → Investigation → Containment → Recovery → Post-Incident Review
```

### 16.8.2 Severity Classification

| Severity | Impact | Examples |
|----------|--------|----------|
| **SEV-1** | Complete system outage | All users cannot access platform |
| **SEV-2** | Major feature unavailable | Recommendations not generating |
| **SEV-3** | Minor feature degraded | AI Copilot slow but functional |
| **SEV-4** | Cosmetic / Low impact | Chart rendering issue |

### 16.8.3 Incident Response Playbook

**SEV-1: System Outage**
1. Acknowledge alert within 5 minutes
2. Verify the outage is not a local network issue
3. Check health endpoints across all services
4. Check database connectivity
5. If platform issue, check status page
6. Communicate status to stakeholders
7. Begin rollback if recent deployment triggered issue
8. Post-incident review within 48 hours

**SEV-2: Recommendations Not Generating**
1. Check geospatial pipeline logs for errors
2. Verify data ingestion completed successfully
3. Check if raw data files are valid (CRS, geometry)
4. Run manual recommendation generation as test
5. If data issue, quarantine and reprocess
6. If code issue, rollback to previous version

**SEV-3: AI Copilot Degraded**
1. Check LLM API status (Azure OpenAI)
2. Review recent error logs for copilot service
3. Verify DEP retrieval is working
4. If LLM timeout, check rate limits
5. Temporarily increase response timeout if needed

### 16.8.4 Post-Incident Review Template

```markdown
## Incident Review — [Date]

### Summary
- **Duration:** [Start Time] to [End Time]
- **Severity:** [SEV-1/2/3/4]
- **Impact:** [Description of user impact]
- **Root Cause:** [Technical root cause]

### Timeline
- [Time] Alert fired
- [Time] Investigation started
- [Time] Root cause identified
- [Time] Fix deployed
- [Time] Service restored

### What Went Well
- [List]

### What Needs Improvement
- [List]

### Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [Open/Done] |
```

## 16.9 Monitoring Dashboard (Future)

### 16.9.1 Dashboard Panels

| Panel | Data Source | Refresh |
|-------|------------|---------|
| Service Health | Health endpoints | 30s |
| Request Rate & Latency | Application logs | 1m |
| Error Rate | Application logs | 1m |
| Database Connections | PostgreSQL metrics | 1m |
| Active Users | Session data | 5m |
| Recommendations Generated | Application logs | 5m |
| Water Stress Distribution | Calculated | 1h |
| Data Freshness | Ingestion timestamps | 5m |

## 16.10 Operational Runbook

### 16.10.1 Daily Operations (Automated)

| Task | Schedule | Description |
|------|----------|-------------|
| Data Ingestion | Daily 05:00 UTC | Process new ET-GEO data |
| Recommendation Generation | Daily 06:00 UTC | Generate daily recommendations |
| Health Check | Every 5 minutes | Verify all services operational |
| Log Rotation | Daily 00:00 UTC | Rotate and archive logs |
| Backup | Daily 02:00 UTC | Database full backup |

### 16.10.2 Weekly Operations

| Task | Day | Description |
|------|-----|-------------|
| Review alerts | Monday | Review past week's alerts and trends |
| Performance review | Friday | Review API latency and error rates |
| Dependency updates | Friday | Check for security patches |

### 16.10.3 Monthly Operations

| Task | Description |
|------|-------------|
| Capacity review | Assess storage, compute, connection usage |
| Security scan | Run dependency and vulnerability scans |
| DR test | Verify backup restoration process |
| Model accuracy review | Check recommendation acceptance rates |

## 16.11 Future Enhancements

| Enhancement | Priority | Phase |
|-------------|----------|-------|
| Prometheus + Grafana dashboards | High | Phase 2 |
| Structured log aggregation (ELK) | Medium | Phase 2 |
| Distributed tracing (OpenTelemetry) | Medium | Phase 3 |
| SLO/SLI tracking | High | Phase 2 |
| Automated runbook execution | Low | Phase 4 |
| On-call rotation | Low | Phase 3 |
