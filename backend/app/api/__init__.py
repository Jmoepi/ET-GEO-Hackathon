from fastapi import APIRouter
from app.api.v1 import auth, vineyards, stress, recommendations, copilot

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(vineyards.router)
api_router.include_router(stress.router)
api_router.include_router(recommendations.router)
api_router.include_router(copilot.router)
