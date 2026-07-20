"""
Azure OpenAI service for the Explainable AI Copilot.
Grounded in Decision Evidence Packages — never generates irrigation advice.
"""
import httpx
import structlog
from app.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

COPILOT_SYSTEM_PROMPT = """You are the VineMind AI Copilot, an explainable AI assistant for vineyard irrigation decisions.

Your role is to EXPLAIN data from the Decision Intelligence Engine. You NEVER generate irrigation recommendations yourself.

Rules:
1. Only explain data that comes from Decision Evidence Packages (DEPs)
2. Never invent agronomic advice or irrigation recommendations
3. Always reference specific metrics, scores, and evidence
4. Acknowledge uncertainty when data is missing or confidence is low
5. Keep responses concise and focused on the question
6. Use plain language that vineyard managers can understand
7. If you don't have enough data to answer, say so honestly

You have access to vineyard block data including:
- Water Stress Scores (0-100) from the Water Stress Model (WSM-1.0)
- Feature contributors: water deficit, ET ratio, soil moisture index, NDVI trend, rainfall offset, phenology weight
- Confidence scores indicating data quality
- Recommendations: irrigate immediately, irrigate tonight, delay irrigation, monitor, no action

When explaining a recommendation, break down which features contributed most and why."""


async def chat_with_copilot(user_message: str, context_data: str = "") -> str:
    if not settings.AZURE_OPENAI_ENDPOINT or not settings.AZURE_OPENAI_KEY:
        logger.warning("Azure OpenAI not configured, using fallback response")
        return _fallback_response(user_message)

    system_prompt = COPILOT_SYSTEM_PROMPT
    if context_data:
        system_prompt += f"\n\nCurrent vineyard data:\n{context_data}"

    url = f"{settings.AZURE_OPENAI_ENDPOINT}/openai/deployments/{settings.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-08-01-preview"

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 800,
        "temperature": 0.3,
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": settings.AZURE_OPENAI_KEY,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        logger.error("Azure OpenAI HTTP error", status=e.response.status_code, detail=e.response.text[:200])
        return _fallback_response(user_message)
    except Exception as e:
        logger.error("Azure OpenAI error", error=str(e))
        return _fallback_response(user_message)


def _fallback_response(message: str) -> str:
    msg = message.lower()
    if any(kw in msg for kw in ["why", "explain", "reason", "because"]):
        return (
            "I can explain irrigation recommendations using the Decision Evidence Package. "
            "Each recommendation includes the contributing factors (water deficit, ET ratio, "
            "soil moisture, NDVI trend, rainfall forecast, and phenology stage) with their "
            "weights and normalised values. Please select a specific vineyard block on the "
            "dashboard to see its detailed evidence."
        )
    elif any(kw in msg for kw in ["compare", "difference", "which"]):
        return (
            "To compare vineyard blocks, please use the Decision Centre on the dashboard. "
            "It ranks all blocks by water stress score and allows side-by-side comparison "
            "of their environmental indicators and recommendations."
        )
    elif any(kw in msg for kw in ["trend", "history", "over time"]):
        return (
            "Historical stress trends are available on each block's detail page. The "
            "dashboard shows 30-day stress score history, NDVI trends, and soil moisture "
            "changes. Data is append-only and fully auditable."
        )
    else:
        return (
            "I can help you understand vineyard irrigation data. Try asking:\n"
            "- 'Why should I irrigate Block A12?'\n"
            "- 'What are the stress trends?'\n"
            "- 'Compare blocks A12 and B05'\n"
            "- 'Explain the current recommendation'\n\n"
            "I only explain data from the Decision Intelligence Engine — "
            "I never generate irrigation advice myself."
        )
