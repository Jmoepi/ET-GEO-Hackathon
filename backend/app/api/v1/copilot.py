from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas import CopilotChatRequest, CopilotChatResponse
from app.models import User, Block, StressScore, Recommendation, DecisionEvidence
from app.services.copilot_service import chat_with_copilot

router = APIRouter(prefix="/copilot", tags=["AI Copilot"])


async def _build_context(db: AsyncSession) -> str:
    blocks_result = await db.execute(select(Block).limit(20))
    blocks = list(blocks_result.scalars().all())

    if not blocks:
        return "No vineyard blocks are currently configured."

    context_parts = ["Vineyard blocks and their current status:"]

    for block in blocks[:10]:
        stress_result = await db.execute(
            select(StressScore)
            .where(StressScore.block_id == block.id)
            .order_by(StressScore.generated_at.desc())
            .limit(1)
        )
        stress = stress_result.scalar_one_or_none()

        rec_result = await db.execute(
            select(Recommendation)
            .where(Recommendation.block_id == block.id)
            .order_by(Recommendation.generated_at.desc())
            .limit(1)
        )
        rec = rec_result.scalar_one_or_none()

        block_info = f"\n- {block.name}"
        if block.cultivar:
            block_info += f" ({block.cultivar})"
        if block.area_ha:
            block_info += f", {block.area_ha}ha"

        if stress:
            block_info += f"\n  Stress Score: {stress.stress_score}/100 ({stress.stress_category})"
            block_info += f", Confidence: {stress.confidence * 100:.0f}%"
            block_info += f", Model: {stress.model_version}"

            if stress.contributors:
                top = sorted(stress.contributors, key=lambda c: c.get("weighted_score", 0), reverse=True)[:3]
                factors = [f"{c.get('metric', 'unknown')}={c.get('raw_value', 0):.2f}" for c in top if c.get("available", True)]
                if factors:
                    block_info += f"\n  Top factors: {', '.join(factors)}"

        if rec:
            block_info += f"\n  Recommendation: {rec.recommendation_type.replace('_', ' ').title()}"
            block_info += f" (confidence: {rec.confidence * 100:.0f}%)"

        context_parts.append(block_info)

    return "\n".join(context_parts)


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

    context = await _build_context(db)
    answer = await chat_with_copilot(request.message, context_data=context)

    return CopilotChatResponse(answer=answer, decision_id=None)
