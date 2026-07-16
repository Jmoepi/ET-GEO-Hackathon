from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "viewer"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class VineyardBase(BaseModel):
    name: str
    area_hectares: Optional[float] = None


class VineyardCreate(VineyardBase):
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    boundary: Optional[str] = None


class VineyardResponse(VineyardBase):
    id: UUID
    owner_id: UUID
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    boundary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BlockBase(BaseModel):
    name: str
    cultivar: Optional[str] = None
    area_ha: Optional[float] = None
    planting_year: Optional[str] = None


class BlockCreate(BlockBase):
    vineyard_id: UUID
    geometry: Optional[str] = None


class BlockResponse(BlockBase):
    id: UUID
    vineyard_id: UUID
    geometry: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ObservationResponse(BaseModel):
    id: UUID
    block_id: UUID
    observation_date: datetime
    eta: Optional[float] = None
    eto: Optional[float] = None
    kc: Optional[float] = None
    ndvi: Optional[float] = None
    soil_moisture: Optional[float] = None
    temperature: Optional[float] = None
    rainfall: Optional[float] = None
    phenology_stage: Optional[str] = None
    data_source: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StressScoreResponse(BaseModel):
    id: UUID
    block_id: UUID
    stress_score: float
    stress_category: str
    confidence: float
    model_version: str
    contributors: list
    generated_at: datetime

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    id: UUID
    block_id: UUID
    recommendation_type: str
    priority: str
    status: str
    explanation: Optional[str] = None
    confidence: float
    generated_at: datetime

    class Config:
        from_attributes = True


class DecisionEvidenceResponse(BaseModel):
    id: UUID
    recommendation_id: UUID
    contributors_json: list
    stress_score: float
    confidence: float
    model_version: str
    decision_rules_triggered: list
    explanation: Optional[str] = None
    generated_at: datetime

    class Config:
        from_attributes = True


class CopilotChatRequest(BaseModel):
    message: str


class CopilotChatResponse(BaseModel):
    answer: str
    decision_id: Optional[str] = None


class ErrorResponse(BaseModel):
    error: dict


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
