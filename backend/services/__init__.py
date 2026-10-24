"""Services package for GitHub integration, analytics, embeddings and matchmaking."""

from backend.services.github_client import github_client, GitHubClient
from backend.services.analyzer import profile_analyzer, ProfileAnalyzer
from backend.services.embedding import embedding_engine, EmbeddingEngine
from backend.services.matchmaker import matchmaker_engine, MatchmakerEngine
from backend.services.collaboration import collaboration_service, CollaborationService
from backend.services.ai_assistant import ai_assistant_service, AIAssistantService

__all__ = [
    "github_client",
    "GitHubClient",
    "profile_analyzer",
    "ProfileAnalyzer",
    "embedding_engine",
    "EmbeddingEngine",
    "matchmaker_engine",
    "MatchmakerEngine",
    "collaboration_service",
    "CollaborationService",
    "ai_assistant_service",
    "AIAssistantService",
]
