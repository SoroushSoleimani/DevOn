"""Integration test suite for FastAPI REST endpoints using TestClient."""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verify health check endpoint returns 200 and valid status."""
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["app"] == "DevOn"
    assert "uptime_seconds" in data


def test_list_community_profiles():
    """Verify community profiles endpoint returns developers list."""
    res = client.get("/api/v1/profiles/community")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    assert any(d["username"] == "SoroushSoleimani" for d in data)


def test_get_specific_developer_profile():
    """Verify fetching developer profile by username."""
    res = client.get("/api/v1/profiles/SoroushSoleimani")
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "SoroushSoleimani"
    assert data["name"] == "Soroush Soleimani"
    assert len(data["top_languages"]) > 0


def test_find_matches_endpoint():
    """Verify matches/find endpoint returns ranked recommendations."""
    res = client.get("/api/v1/matches/find/SoroushSoleimani?pairing_mode=complementary")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    top_match = data[0]
    assert "overall_score" in top_match
    assert top_match["overall_score"] >= 40.0
    assert "breakdown" in top_match


def test_compare_developers_endpoint():
    """Verify side-by-side comparison endpoint."""
    res = client.get("/api/v1/matches/compare?developer_a=SoroushSoleimani&developer_b=elena-codes")
    assert res.status_code == 200
    data = res.json()
    assert data["developer_a"]["username"] == "SoroushSoleimani"
    assert data["developer_b"]["username"] == "elena-codes"
    assert "breakdown" in data
    assert len(data["synergy_highlights"]) > 0


def test_collaboration_ideas_endpoint():
    """Verify project ideas generation between two developers."""
    res = client.get("/api/v1/collaboration/ideas?developer_a=SoroushSoleimani&developer_b=elena-codes")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert "recommended_tech_stack" in data[0]


def test_collaboration_pitch_endpoint():
    """Verify pitch generation endpoint."""
    res = client.get("/api/v1/collaboration/pitch?developer_a=SoroushSoleimani&developer_b=elena-codes")
    assert res.status_code == 200
    data = res.json()
    assert data["developer_a_username"] == "SoroushSoleimani"
    assert "Elena" in data["icebreaker_text"]


def test_ai_chat_assistant_endpoint():
    """Verify AI assistant chat endpoint."""
    payload = {
        "developer_username": "SoroushSoleimani",
        "candidate_username": "elena-codes",
        "messages": [{"role": "user", "content": "How do our timezones align?"}],
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert len(data["suggested_actions"]) > 0


def test_auth_me_endpoint():
    """Verify /auth/me returns default or authenticated profile."""
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "SoroushSoleimani"
