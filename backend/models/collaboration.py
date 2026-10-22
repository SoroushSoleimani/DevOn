"""Pydantic models for Collaboration ideas, issue suggestions, and AI pitches."""

from typing import List, Optional
from pydantic import BaseModel, Field


class PairProjectIdea(BaseModel):
    """Idea for a collaborative pair programming project."""
    title: str
    description: str
    recommended_tech_stack: List[str]
    developer_a_role: str
    developer_b_role: str
    estimated_difficulty: str = "Intermediate"
    why_good_fit: str


class RecommendedIssue(BaseModel):
    """Recommended open source issue or repository to work on together."""
    repo_name: str
    repo_url: str
    issue_title: str
    issue_url: str
    labels: List[str] = Field(default_factory=list)
    relevance_reason: str


class CollaborationPitch(BaseModel):
    """Generated outreach pitch / icebreaker to initiate pairing."""
    developer_a_username: str
    developer_b_username: str
    icebreaker_text: str
    pitch_subject: str
    suggested_project_ideas: List[PairProjectIdea] = Field(default_factory=list)
    recommended_schedule_slots: List[str] = Field(default_factory=list)


class AIChatMessage(BaseModel):
    """Message for AI Pair Programming Assistant."""
    role: str  # 'user', 'assistant', 'system'
    content: str


class AIChatRequest(BaseModel):
    """Request to the DevOn AI Match Assistant."""
    developer_username: str
    candidate_username: Optional[str] = None
    messages: List[AIChatMessage]
    pairing_mode: Optional[str] = "complementary"


class AIChatResponse(BaseModel):
    """Response from AI Assistant with suggestions and insights."""
    reply: str
    suggested_actions: List[str] = Field(default_factory=list)
