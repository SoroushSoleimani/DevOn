"""Services package for GitHub integration, analytics, embeddings and matchmaking."""

from backend.services.github_client import github_client, GitHubClient
from backend.services.analyzer import profile_analyzer, ProfileAnalyzer

__all__ = ["github_client", "GitHubClient", "profile_analyzer", "ProfileAnalyzer"]
