from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import User, Vineyard, Block, Observation, StressScore, Recommendation, DecisionEvidence


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, name: str, email: str, password_hash: str, role: str = "viewer") -> User:
    user = User(name=name, email=email, password_hash=password_hash, role=role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_vineyards(db: AsyncSession, owner_id: UUID | None = None) -> list[Vineyard]:
    stmt = select(Vineyard).options(selectinload(Vineyard.blocks))
    if owner_id:
        stmt = stmt.where(Vineyard.owner_id == owner_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_vineyard_by_id(db: AsyncSession, vineyard_id: UUID) -> Vineyard | None:
    result = await db.execute(
        select(Vineyard)
        .options(selectinload(Vineyard.blocks))
        .where(Vineyard.id == vineyard_id)
    )
    return result.scalar_one_or_none()


async def create_vineyard(db: AsyncSession, **kwargs) -> Vineyard:
    vineyard = Vineyard(**kwargs)
    db.add(vineyard)
    await db.commit()
    await db.refresh(vineyard)
    return vineyard


async def get_blocks(db: AsyncSession, vineyard_id: UUID | None = None) -> list[Block]:
    stmt = select(Block)
    if vineyard_id:
        stmt = stmt.where(Block.vineyard_id == vineyard_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_block_by_id(db: AsyncSession, block_id: UUID) -> Block | None:
    result = await db.execute(select(Block).where(Block.id == block_id))
    return result.scalar_one_or_none()


async def create_block(db: AsyncSession, **kwargs) -> Block:
    block = Block(**kwargs)
    db.add(block)
    await db.commit()
    await db.refresh(block)
    return block


async def get_latest_observation(db: AsyncSession, block_id: UUID) -> Observation | None:
    result = await db.execute(
        select(Observation)
        .where(Observation.block_id == block_id)
        .order_by(Observation.observation_date.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_observation_history(db: AsyncSession, block_id: UUID, days: int = 30) -> list[Observation]:
    result = await db.execute(
        select(Observation)
        .where(Observation.block_id == block_id)
        .order_by(Observation.observation_date.desc())
        .limit(days)
    )
    return list(result.scalars().all())


async def create_observation(db: AsyncSession, **kwargs) -> Observation:
    obs = Observation(**kwargs)
    db.add(obs)
    await db.commit()
    await db.refresh(obs)
    return obs


async def get_latest_stress_score(db: AsyncSession, block_id: UUID) -> StressScore | None:
    result = await db.execute(
        select(StressScore)
        .where(StressScore.block_id == block_id)
        .order_by(StressScore.generated_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_stress_history(db: AsyncSession, block_id: UUID, days: int = 30) -> list[StressScore]:
    result = await db.execute(
        select(StressScore)
        .where(StressScore.block_id == block_id)
        .order_by(StressScore.generated_at.desc())
        .limit(days)
    )
    return list(result.scalars().all())


async def create_stress_score(db: AsyncSession, **kwargs) -> StressScore:
    score = StressScore(**kwargs)
    db.add(score)
    await db.commit()
    await db.refresh(score)
    return score


async def get_recommendations(db: AsyncSession, status: str | None = None) -> list[Recommendation]:
    stmt = select(Recommendation).options(
        selectinload(Recommendation.block),
        selectinload(Recommendation.decision_evidence),
    )
    if status:
        stmt = stmt.where(Recommendation.status == status)
    result = await db.execute(stmt.order_by(Recommendation.generated_at.desc()))
    return list(result.scalars().all())


async def get_recommendation_by_block(db: AsyncSession, block_id: UUID) -> Recommendation | None:
    result = await db.execute(
        select(Recommendation)
        .options(selectinload(Recommendation.decision_evidence))
        .where(Recommendation.block_id == block_id)
        .order_by(Recommendation.generated_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def create_recommendation(db: AsyncSession, **kwargs) -> Recommendation:
    rec = Recommendation(**kwargs)
    db.add(rec)
    await db.commit()
    await db.refresh(rec)
    return rec


async def create_decision_evidence(db: AsyncSession, **kwargs) -> DecisionEvidence:
    evidence = DecisionEvidence(**kwargs)
    db.add(evidence)
    await db.commit()
    await db.refresh(evidence)
    return evidence
