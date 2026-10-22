"""Pydantic models for Matchmaking requests, scores, and responses."""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from backend.models.developer import DeveloperProfile, PrimaryRole, ExperienceTier, CodingRhythm


class PairingMode(str, Enum):
    """Strategy used for matching developers."""
    COMPLEMENTARY = "complementary"  # Pair opposite strengths (frontend + backend)
    SIMILAR = "similar"              # Pair like-minded stack (python + python)
    PEER_LEARNING = "peer_learning"  # Pair similar experience for parallel exploration
    MENTORSHIP = "mentorship"        # Pair senior with junior/mid


class CompatibilityBreakdown(BaseModel):
    """Granular breakdown of compatibility factors."""
    skill_complementarity: float = Field(0.0, description="0.0 - 100.0 score")
    schedule_compatibility: float = Field(0.0, description="0.0 - 100.0 score")
    domain_interests_overlap: float = Field(0.0, description="0.0 - 100.0 score")
    experience_tier_synergy: float = Field(0.0, description="0.0 - 100.0 score")
    semantic_vector_similarity: float = Field(0.0, description="0.0 - 100.0 score")


class MatchFilter(BaseModel):
    """Filtering criteria for finding coding partners."""
    target_language: Optional[str] = None
    primary_role: Optional[PrimaryRole] = None
    experience_tier: Optional[ExperienceTier] = None
    coding_rhythm: Optional[CodingRhythm] = None
    pairing_mode: PairingMode = PairingMode.COMPLEMENTARY
    max_timezone_diff_hours: Optional[float] = None
    min_compatibility_score: float = 50.0
    limit: int = 10


class MatchResult(BaseModel):
    """Result of matching target developer against candidate partner."""
    developer: DeveloperProfile
    overall_score: float = Field(0.0, description="Overall compatibility percentage 0-100%")
    breakdown: CompatibilityBreakdown
    pairing_mode: PairingMode = PairingMode.COMPLEMENTARY
    synergy_reasons: List[str] = Field(default_factory=list)
    shared_interests: List[str] = Field(default_factory=list)
    complementary_skills: List[str] = Field(default_factory=list)
    potential_collaboration_topics: List[str] = Field(default_factory=list)


class DeveloperComparison(BaseModel):
    """Direct side-by-side comparison of two developers."""
    developer_a: DeveloperProfile
    developer_b: DeveloperProfile
    overall_compatibility: float
    breakdown: CompatibilityBreakdown
    synergy_highlights: List[str]
    potential_friction_points: List[str] = Field(default_factory=list)
    suggested_focus: str
