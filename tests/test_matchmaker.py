"""Unit and integration tests for matchmaking engine and collaboration generator."""

import asyncio
import pytest
from backend.models.developer import PrimaryRole, CodingRhythm, ExperienceTier
from backend.models.matching import MatchFilter, PairingMode
from backend.models.collaboration import AIChatRequest, AIChatMessage
from backend.services.github_client import github_client
from backend.services.matchmaker import matchmaker_engine
from backend.services.collaboration import collaboration_service
from backend.services.ai_assistant import ai_assistant_service


def test_evaluate_pair_complementary_synergy():
    """Verify backend and frontend developers achieve strong complementary scores."""
    dev_backend = asyncio.run(github_client.get_developer_profile("SoroushSoleimani"))
    dev_frontend = asyncio.run(github_client.get_developer_profile("elena-codes"))

    result = asyncio.run(matchmaker_engine.evaluate_pair(dev_backend, dev_frontend, PairingMode.COMPLEMENTARY))

    assert result.overall_score >= 80.0
    assert result.breakdown.skill_complementarity >= 90.0
    assert len(result.synergy_reasons) > 0
    assert result.developer.username == "elena-codes"


def test_find_matches_for_user():
    """Verify matchmaking returns ranked list of compatible developers excluding self."""
    results = asyncio.run(matchmaker_engine.find_matches_for_user("SoroushSoleimani"))

    assert len(results) > 0
    # Candidate should not be the user themselves
    assert all(r.developer.username != "SoroushSoleimani" for r in results)
    # Sorted descending by score
    scores = [r.overall_score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_find_matches_filter_role():
    """Verify primary_role filter returns only candidates with requested role."""
    match_filter = MatchFilter(primary_role=PrimaryRole.FRONTEND)
    results = asyncio.run(matchmaker_engine.find_matches_for_user("SoroushSoleimani", match_filter))

    assert len(results) > 0
    assert all(r.developer.primary_role == PrimaryRole.FRONTEND for r in results)


def test_find_matches_filter_language():
    """Verify target_language filter matches correctly."""
    match_filter = MatchFilter(target_language="TypeScript")
    results = asyncio.run(matchmaker_engine.find_matches_for_user("SoroushSoleimani", match_filter))

    assert len(results) > 0
    for r in results:
        langs = [l.language.lower() for l in r.developer.top_languages]
        assert "typescript" in langs


def test_developer_comparison():
    """Verify side-by-side comparison generates breakdown and highlights."""
    comparison = asyncio.run(matchmaker_engine.compare_developers("SoroushSoleimani", "elena-codes"))

    assert comparison.developer_a.username == "SoroushSoleimani"
    assert comparison.developer_b.username == "elena-codes"
    assert comparison.overall_compatibility >= 75.0
    assert len(comparison.synergy_highlights) > 0


def test_collaboration_pitch_generator():
    """Verify collaboration pitch contains personalized icebreaker and project ideas."""
    dev_a = asyncio.run(github_client.get_developer_profile("SoroushSoleimani"))
    dev_b = asyncio.run(github_client.get_developer_profile("elena-codes"))

    pitch = collaboration_service.generate_collaboration_pitch(dev_a, dev_b)

    assert pitch.developer_a_username == "SoroushSoleimani"
    assert pitch.developer_b_username == "elena-codes"
    assert "Elena" in pitch.icebreaker_text
    assert len(pitch.suggested_project_ideas) >= 2


def test_ai_assistant_icebreaker():
    """Verify AI assistant generates contextual icebreaker response."""
    req = AIChatRequest(
        developer_username="SoroushSoleimani",
        candidate_username="elena-codes",
        messages=[AIChatMessage(role="user", content="Help me draft an outreach icebreaker")],
    )
    res = asyncio.run(ai_assistant_service.process_chat(req))

    assert len(res.reply) > 20
    assert len(res.suggested_actions) > 0
