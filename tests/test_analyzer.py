"""Unit tests for developer profile analyzer and rhythm metrics."""

import pytest
from backend.models.developer import (
    DeveloperProfile,
    LanguageStat,
    CodingRhythm,
    PrimaryRole,
)
from backend.services.analyzer import ProfileAnalyzer


def test_classify_role_distribution():
    """Verify language distributions map accurately to domains."""
    languages = [
        LanguageStat(language="TypeScript", percentage=60.0),
        LanguageStat(language="CSS", percentage=40.0),
    ]
    distribution = ProfileAnalyzer.classify_role_distribution(languages)

    assert distribution["frontend"] > 90.0
    assert distribution["systems"] == 0.0


def test_compute_rhythm_night_owl():
    """Verify high night-owl score correctly categorizes as NIGHT_OWL."""
    rhythm, breakdown = ProfileAnalyzer.compute_rhythm_profile(
        night_owl_score=0.85, weekend_ratio=0.25
    )
    assert rhythm == CodingRhythm.NIGHT_OWL
    assert breakdown["night"] > 25.0


def test_compute_rhythm_early_bird():
    """Verify low night-owl score correctly categorizes as EARLY_BIRD."""
    rhythm, breakdown = ProfileAnalyzer.compute_rhythm_profile(
        night_owl_score=0.20, weekend_ratio=0.20
    )
    assert rhythm == CodingRhythm.EARLY_BIRD
    assert breakdown["morning"] > 30.0


def test_compute_rhythm_weekend_warrior():
    """Verify high weekend commit ratio categorizes as WEEKEND_WARRIOR."""
    rhythm, _ = ProfileAnalyzer.compute_rhythm_profile(
        night_owl_score=0.50, weekend_ratio=0.48
    )
    assert rhythm == CodingRhythm.WEEKEND_WARRIOR


def test_enrich_profile():
    """Verify enrich_profile augments skill tags and AI summary."""
    profile = DeveloperProfile(
        username="testdev",
        avatar_url="http://example.com/avatar.png",
        primary_role=PrimaryRole.BACKEND,
        top_languages=[LanguageStat(language="Python", percentage=100.0)],
        night_owl_score=0.8,
        weekend_activity_ratio=0.2,
    )
    enriched = ProfileAnalyzer.enrich_profile(profile)

    assert "Python" in enriched.skill_tags
    assert enriched.coding_rhythm == CodingRhythm.NIGHT_OWL
    assert enriched.ai_summary is not None
    assert "testdev" in enriched.ai_summary
