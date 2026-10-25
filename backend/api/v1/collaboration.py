"""Collaboration endpoints for pair project ideas and outreach pitches."""

from typing import List
from fastapi import APIRouter, HTTPException, Query
from backend.models.collaboration import (
    PairProjectIdea,
    CollaborationPitch,
)
from backend.services.github_client import github_client
from backend.services.analyzer import profile_analyzer
from backend.services.collaboration import collaboration_service

router = APIRouter()


@router.get("/ideas", response_model=List[PairProjectIdea])
async def get_pair_project_ideas(
    developer_a: str = Query(..., description="First developer username"),
    developer_b: str = Query(..., description="Second developer username"),
):
    """Generate collaborative project concepts tailored to both developers' skillsets."""
    try:
        dev_a = await github_client.get_developer_profile(developer_a)
        dev_b = await github_client.get_developer_profile(developer_b)
        dev_a = profile_analyzer.enrich_profile(dev_a)
        dev_b = profile_analyzer.enrich_profile(dev_b)
        return collaboration_service.generate_project_ideas(dev_a, dev_b)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")


@router.get("/pitch", response_model=CollaborationPitch)
async def generate_pitch(
    developer_a: str = Query(..., description="Sender developer username"),
    developer_b: str = Query(..., description="Recipient developer username"),
):
    """Generate high-converting collaboration pitch and outreach icebreaker."""
    try:
        dev_a = await github_client.get_developer_profile(developer_a)
        dev_b = await github_client.get_developer_profile(developer_b)
        dev_a = profile_analyzer.enrich_profile(dev_a)
        dev_b = profile_analyzer.enrich_profile(dev_b)
        return collaboration_service.generate_collaboration_pitch(dev_a, dev_b)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating pitch: {str(e)}")
