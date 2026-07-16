from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas import StressScoreResponse
from app.services import get_latest_stress_score, get_stress_history, get_latest_observation, create_stress_score, create_observation
from app.decision_engine.water_stress_model import BlockObservation, calculate_stress, score_to_recommendation
from app.models import User

router = APIRouter(prefix="/stress", tags=["Water Stress"])


@router.get("/{block_id}", response_model=StressScoreResponse)
async def get_block_stress(
    block_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    score = await get_latest_stress_score(db, block_id)
    if not score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No stress score found for this block",
        )
    return score


@router.get("/history/{block_id}", response_model=list[StressScoreResponse])
async def get_block_stress_history(
    block_id: UUID,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    scores = await get_stress_history(db, block_id, days=days)
    return scores


@router.post("/calculate/{block_id}", response_model=StressScoreResponse)
async def calculate_block_stress(
    block_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    observation = await get_latest_observation(db, block_id)
    if not observation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No observation found for this block. Ingest observation data first.",
        )

    previous_obs = await get_stress_history(db, block_id, days=2)
    ndvi_previous = previous_obs[1].ndvi if len(previous_obs) > 1 else observation.ndvi

    block_obs = BlockObservation(
        block_id=str(block_id),
        observation_date=observation.observation_date,
        eta=observation.eta,
        eto=observation.eto,
        kc=observation.kc,
        ndvi=observation.ndvi,
        ndvi_previous=ndvi_previous,
        soil_moisture=observation.soil_moisture,
        rainfall_forecast=observation.rainfall,
        temperature=observation.temperature,
        phenology_stage=observation.phenology_stage,
    )

    result = calculate_stress(block_obs)

    stress_score = await create_stress_score(
        db,
        observation_id=observation.id,
        block_id=block_id,
        stress_score=result.stress_score,
        stress_category=result.stress_category.value,
        confidence=result.confidence,
        model_version=result.model_version,
        contributors=[{
            "metric": c.metric,
            "value": c.raw_value,
            "normalised": c.normalised_value,
            "weight": c.weight,
            "weighted_score": c.weighted_score,
            "unit": c.unit,
            "available": c.available,
        } for c in result.contributors],
    )

    return stress_score
