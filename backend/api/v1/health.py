"""Health check endpoint and system status."""

import time
from fastapi import APIRouter
from backend.core.config import settings

router = APIRouter()
START_TIME = time.time()


@router.get("")
async def get_health_status():
    """Return system health status, version, and runtime uptime."""
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": round(time.time() - START_TIME, 1),
    }
