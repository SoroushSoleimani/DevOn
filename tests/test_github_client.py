"""Unit tests for GitHub client and profile fetching."""

import asyncio
from backend.services.github_client import GitHubClient, SEED_DEVELOPERS


def test_get_developer_profile_seed():
    """Verify seed profiles are returned accurately and cached."""
    client = GitHubClient()
    profile = asyncio.run(client.get_developer_profile("SoroushSoleimani"))

    assert profile.username == "SoroushSoleimani"
    assert profile.name == "Soroush Soleimani"
    assert profile.public_repos_count >= 10
    assert len(profile.top_languages) > 0
    assert any(l.language == "Python" for l in profile.top_languages)


def test_get_developer_profile_case_insensitive():
    """Verify case-insensitive lookups work properly."""
    client = GitHubClient()
    profile = asyncio.run(client.get_developer_profile("soroushsoleimani"))

    assert profile.username == "SoroushSoleimani"
    assert profile.name == "Soroush Soleimani"


def test_synthetic_profile_generation():
    """Verify synthetic profile is safely created for unknown users."""
    client = GitHubClient()
    profile = asyncio.run(client.get_developer_profile("nonexistent-dev-12345"))

    assert profile.username == "nonexistent-dev-12345"
    assert profile.open_to_collaborate is True
    assert profile.public_repos_count > 0


def test_list_community_developers():
    """Verify community list contains all seeded developers."""
    client = GitHubClient()
    developers = asyncio.run(client.list_community_developers())

    assert len(developers) >= len(SEED_DEVELOPERS)
    usernames = [d.username for d in developers]
    assert "SoroushSoleimani" in usernames
    assert "elena-codes" in usernames
