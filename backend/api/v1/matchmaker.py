"""Matchmaking and developer comparison endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from backend.models.developer import PrimaryRole, ExperienceTier, CodingRhythm
from backend.models.matching import (
    MatchResult,
    MatchFilter,
    DeveloperComparison,
    PairingMode,
)
from backend.services.matchmaker import matchmaker_engine

router = APIRouter()


@router.get("/find/{username}", response_model=List[MatchResult])
async def find_matches(
    username: str,
    pairing_mode: PairingMode = Query(PairingMode.COMPLEMENTARY, description="Matching strategy"),
    target_language: Optional[str] = Query(None, description="Filter candidates by language"),
    primary_role: Optional[PrimaryRole] = Query(None, description="Filter candidates by role"),
    coding_rhythm: Optional[CodingRhythm] = Query(None, description="Filter candidates by schedule"),
    min_score: float = Query(40.0, ge=0.0, le=100.0, description="Minimum compatibility score"),
    limit: int = Query(10, ge=1, le=50, description="Max matches to return"),
):
    """Find ranked developer matches for a given GitHub username."""
    match_filter = MatchFilter(
        pairing_mode=pairing_mode,
        target_language=target_language,
        primary_role=primary_role,
        coding_rhythm=coding_rhythm,
        min_compatibility_score=min_score,
        limit=limit,
    )
    try:
        return await matchmaker_engine.find_matches_for_user(username, match_filter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matchmaking error: {str(e)}")


@router.get("/compare", response_model=DeveloperComparison)
async def compare_developers(
    developer_a: str = Query(..., description="First developer username"),
    developer_b: str = Query(..., description="Second developer username"),
):
    """Perform side-by-side comparison between two developers."""
    try:
        return await matchmaker_engine.compare_developers(developer_a, developer_b)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")
