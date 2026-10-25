"""Developer profile endpoints: lookup, live GitHub analysis, and community list."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from backend.models.developer import DeveloperProfile, PrimaryRole, ExperienceTier
from backend.services.github_client import github_client
from backend.services.analyzer import profile_analyzer

router = APIRouter()


@router.get("/community", response_model=List[DeveloperProfile])
async def list_community_developers(
    role: Optional[PrimaryRole] = Query(None, description="Filter by primary role"),
    tier: Optional[ExperienceTier] = Query(None, description="Filter by experience tier"),
):
    """Retrieve all available community developers with optional filtering."""
    developers = await github_client.list_community_developers()
    enriched = [profile_analyzer.enrich_profile(d) for d in developers]

    if role:
        enriched = [d for d in enriched if d.primary_role == role]
    if tier:
        enriched = [d for d in enriched if d.experience_tier == tier]

    return enriched


@router.get("/{username}", response_model=DeveloperProfile)
async def get_developer_profile(username: str):
    """Fetch and synthesize analyzed developer profile from GitHub username."""
    try:
        profile = await github_client.get_developer_profile(username)
        return profile_analyzer.enrich_profile(profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")
