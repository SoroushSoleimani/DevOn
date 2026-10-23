"""Services package for GitHub integration, analytics, embeddings and matchmaking."""

from backend.services.github_client import github_client, GitHubClient

__all__ = ["github_client", "GitHubClient"]
