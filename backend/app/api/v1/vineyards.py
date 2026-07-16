from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas import VineyardCreate, VineyardResponse, BlockCreate, BlockResponse
from app.services import get_vineyards, get_vineyard_by_id, create_vineyard, get_blocks, get_block_by_id, create_block
from app.models import User

router = APIRouter(tags=["Vineyards"])


@router.get("/vineyards", response_model=list[VineyardResponse])
async def list_vineyards(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    vineyards = await get_vineyards(db, owner_id=user.id)
    return vineyards


@router.get("/vineyards/{vineyard_id}", response_model=VineyardResponse)
async def get_vineyard(
    vineyard_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    vineyard = await get_vineyard_by_id(db, vineyard_id)
    if not vineyard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vineyard not found")
    return vineyard


@router.post("/vineyards", response_model=VineyardResponse, status_code=status.HTTP_201_CREATED)
async def add_vineyard(
    request: VineyardCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    vineyard = await create_vineyard(
        db,
        name=request.name,
        owner_id=user.id,
        location_lat=request.location_lat,
        location_lon=request.location_lon,
        boundary=request.boundary,
        area_hectares=request.area_hectares,
    )
    return vineyard


@router.get("/blocks", response_model=list[BlockResponse])
async def list_blocks(
    vineyard_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    blocks = await get_blocks(db, vineyard_id=vineyard_id)
    return blocks


@router.get("/blocks/{block_id}", response_model=BlockResponse)
async def get_block(
    block_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    block = await get_block_by_id(db, block_id)
    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")
    return block


@router.post("/blocks", response_model=BlockResponse, status_code=status.HTTP_201_CREATED)
async def add_block(
    request: BlockCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    block = await create_block(
        db,
        vineyard_id=request.vineyard_id,
        name=request.name,
        cultivar=request.cultivar,
        area_ha=request.area_ha,
        geometry=request.geometry,
        planting_year=request.planting_year,
    )
    return block
