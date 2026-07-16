from uuid import UUID
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas import RecommendationResponse, DecisionEvidenceResponse
from app.services import get_recommendations, get_recommendation_by_block
from app.models import User, DecisionEvidence

router = APIRouter(tags=["Recommendations"])


@router.get("/recommendations", response_model=list[RecommendationResponse])
async def list_recommendations(
    rec_status: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    recs = await get_recommendations(db, status=rec_status)
    return recs


@router.get("/recommendations/{block_id}", response_model=RecommendationResponse)
async def get_block_recommendation(
    block_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rec = await get_recommendation_by_block(db, block_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recommendation found for this block",
        )
    return rec


@router.get("/evidence/{block_id}", response_model=DecisionEvidenceResponse)
async def get_block_evidence(
    block_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rec = await get_recommendation_by_block(db, block_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recommendation found for this block",
        )
    result = await db.execute(
        select(DecisionEvidence).where(DecisionEvidence.recommendation_id == rec.id)
    )
    dep = result.scalar_one_or_none()
    if not dep:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No decision evidence found for this recommendation",
        )
    return dep
