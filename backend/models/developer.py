"""Pydantic data models for Developer Profiles and GitHub activity."""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ExperienceTier(str, Enum):
    """Developer experience level."""
    BEGINNER = "Junior / Beginner"
    INTERMEDIATE = "Mid-Level"
    SENIOR = "Senior"
    STAFF = "Lead / Staff"


class PrimaryRole(str, Enum):
    """Developer primary domain role."""
    FRONTEND = "Frontend Developer"
    BACKEND = "Backend Developer"
    FULLSTACK = "Full Stack Engineer"
    SYSTEMS = "Systems / Low-Level"
    AIML = "AI / Machine Learning"
    DEVOPS = "DevOps & Cloud"
    MOBILE = "Mobile Developer"


class CodingRhythm(str, Enum):
    """Primary active coding schedule habit."""
    NIGHT_OWL = "Night Owl (Late Night)"
    EARLY_BIRD = "Early Bird (Morning)"
    AFTERNOON_PEAK = "Afternoon Peak"
    WEEKEND_WARRIOR = "Weekend Focus"
    BALANCED = "Steady All-Day"


class LanguageStat(BaseModel):
    """Programming language usage metrics."""
    language: str
    bytes_count: int = 0
    percentage: float = 0.0
    repo_count: int = 0


class RepositorySummary(BaseModel):
    """Summary of a developer's public repository."""
    name: str
    description: Optional[str] = None
    html_url: str
    language: Optional[str] = None
    stargazers_count: int = 0
    forks_count: int = 0
    topics: List[str] = Field(default_factory=list)
    is_fork: bool = False
    updated_at: Optional[str] = None


class DeveloperProfile(BaseModel):
    """Comprehensive developer profile synthesized from GitHub activity and preferences."""
    username: str
    name: Optional[str] = None
    avatar_url: str
    bio: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    timezone_offset_hours: float = 0.0
    public_repos_count: int = 0
    total_stars_received: int = 0
    followers_count: int = 0
    following_count: int = 0

    # Skills & Roles
    primary_role: PrimaryRole = PrimaryRole.FULLSTACK
    experience_tier: ExperienceTier = ExperienceTier.INTERMEDIATE
    top_languages: List[LanguageStat] = Field(default_factory=list)
    skill_tags: List[str] = Field(default_factory=list)
    domain_interests: List[str] = Field(default_factory=list)

    # Activity & Work Rhythm
    coding_rhythm: CodingRhythm = CodingRhythm.BALANCED
    night_owl_score: float = Field(0.5, description="0.0 = extreme early bird, 1.0 = extreme night owl")
    weekend_activity_ratio: float = Field(0.3, description="Ratio of weekend commits to total commits")
    active_hours_breakdown: Dict[str, float] = Field(
        default_factory=lambda: {"morning": 25.0, "afternoon": 40.0, "evening": 25.0, "night": 10.0}
    )

    # Repositories & Collaboration Status
    featured_repos: List[RepositorySummary] = Field(default_factory=list)
    open_to_collaborate: bool = True
    preferred_pairing_mode: str = "complementary"  # 'complementary' or 'similar'

    # AI profile summary / pitch
    ai_summary: Optional[str] = None
