"""API v1 router assembly."""

from fastapi import APIRouter
from backend.api.v1.health import router as health_router
from backend.api.v1.auth import router as auth_router
from backend.api.v1.profiles import router as profiles_router
from backend.api.v1.matchmaker import router as matchmaker_router
from backend.api.v1.collaboration import router as collaboration_router
from backend.api.v1.ai_assistant import router as ai_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, prefix="/health", tags=["Health"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])
api_v1_router.include_router(matchmaker_router, prefix="/matches", tags=["Matchmaker"])
api_v1_router.include_router(collaboration_router, prefix="/collaboration", tags=["Collaboration"])
api_v1_router.include_router(ai_router, prefix="/ai", tags=["AI Assistant"])
