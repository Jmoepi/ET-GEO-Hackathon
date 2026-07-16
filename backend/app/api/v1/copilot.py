from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas import CopilotChatRequest, CopilotChatResponse
from app.models import User

router = APIRouter(prefix="/copilot", tags=["AI Copilot"])


@router.post("/chat", response_model=CopilotChatResponse)
async def copilot_chat(
    request: CopilotChatRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )

    message_lower = request.message.lower()

    if any(kw in message_lower for kw in ["why", "explain", "reason", "because"]):
        return CopilotChatResponse(
            answer="I can explain irrigation recommendations using the Decision Evidence Package. Each recommendation includes the contributing factors (water deficit, ET ratio, soil moisture, NDVI trend, rainfall forecast, and phenology stage) with their weights and normalised values. Please select a specific vineyard block on the dashboard to see its detailed evidence.",
            decision_id=None,
        )
    elif any(kw in message_lower for kw in ["compare", "difference", "which"]):
        return CopilotChatResponse(
            answer="To compare vineyard blocks, please use the Decision Centre on the dashboard. It ranks all blocks by water stress score and allows side-by-side comparison of their environmental indicators and recommendations.",
            decision_id=None,
        )
    elif any(kw in message_lower for kw in ["trend", "history", "over time"]):
        return CopilotChatResponse(
            answer="Historical stress trends are available on each block's detail page. The dashboard shows 30-day stress score history, NDVI trends, and soil moisture changes. Data is append-only and fully auditable.",
            decision_id=None,
        )
    else:
        return CopilotChatResponse(
            answer="I can help you understand vineyard irrigation data. Try asking:\n- 'Why should I irrigate Block A12?'\n- 'What are the stress trends?'\n- 'Compare blocks A12 and B05'\n- 'Explain the current recommendation'\n\nI only explain data from the Decision Intelligence Engine — I never generate irrigation advice myself.",
            decision_id=None,
        )
