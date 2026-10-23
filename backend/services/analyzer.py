"""Developer profile analyzer: extracts coding rhythm, role classification, and synergy metrics."""

from typing import Dict, List, Set, Tuple
from backend.models.developer import (
    DeveloperProfile,
    LanguageStat,
    PrimaryRole,
    CodingRhythm,
    ExperienceTier,
)

# Language domain taxonomies
FRONTEND_LANGUAGES = {"javascript", "typescript", "html", "css", "vue", "svelte", "sass", "scss", "coffeescript"}
BACKEND_LANGUAGES = {"python", "java", "c#", "php", "ruby", "go", "node", "kotlin", "scala", "elixir"}
SYSTEMS_LANGUAGES = {"c", "c++", "rust", "zig", "assembly", "fortran", "cuda"}
AIML_LANGUAGES = {"python", "jupyter notebook", "r", "julia", "matlab"}
MOBILE_LANGUAGES = {"dart", "swift", "kotlin", "objective-c"}
DEVOPS_LANGUAGES = {"shell", "bash", "hcl", "dockerfile", "makefile", "powershell"}


class ProfileAnalyzer:
    """Analyzes GitHub profiles to derive role classification, work rhythms, and collaboration traits."""

    @staticmethod
    def classify_role_distribution(languages: List[LanguageStat]) -> Dict[str, float]:
        """Compute percentage breakdown across engineering disciplines."""
        distribution = {
            "frontend": 0.0,
            "backend": 0.0,
            "systems": 0.0,
            "aiml": 0.0,
            "mobile": 0.0,
            "devops": 0.0,
        }

        total_pct = sum(l.percentage for l in languages) or 100.0

        for stat in languages:
            lang_lower = stat.language.lower()
            weight = stat.percentage / total_pct

            if lang_lower in FRONTEND_LANGUAGES:
                distribution["frontend"] += weight
            if lang_lower in BACKEND_LANGUAGES:
                distribution["backend"] += weight
            if lang_lower in SYSTEMS_LANGUAGES:
                distribution["systems"] += weight
            if lang_lower in AIML_LANGUAGES:
                distribution["aiml"] += weight
            if lang_lower in MOBILE_LANGUAGES:
                distribution["mobile"] += weight
            if lang_lower in DEVOPS_LANGUAGES:
                distribution["devops"] += weight

        # Normalize to 100%
        sum_weights = sum(distribution.values()) or 1.0
        return {k: round((v / sum_weights) * 100.0, 1) for k, v in distribution.items()}

    @staticmethod
    def compute_rhythm_profile(
        night_owl_score: float, weekend_ratio: float
    ) -> Tuple[CodingRhythm, Dict[str, float]]:
        """Calculate hour breakdown and dominant rhythm enum."""
        # Baseline distributions influenced by night_owl_score (0.0=morning, 1.0=night)
        night_pct = 5.0 + (night_owl_score * 35.0)       # 5% to 40%
        morning_pct = 40.0 - (night_owl_score * 30.0)    # 10% to 40%
        evening_pct = 25.0 + (night_owl_score * 10.0)    # 25% to 35%
        afternoon_pct = max(10.0, 100.0 - (night_pct + morning_pct + evening_pct))

        breakdown = {
            "morning": round(morning_pct, 1),
            "afternoon": round(afternoon_pct, 1),
            "evening": round(evening_pct, 1),
            "night": round(night_pct, 1),
        }

        if weekend_ratio >= 0.42:
            rhythm = CodingRhythm.WEEKEND_WARRIOR
        elif night_owl_score >= 0.70:
            rhythm = CodingRhythm.NIGHT_OWL
        elif night_owl_score <= 0.30:
            rhythm = CodingRhythm.EARLY_BIRD
        elif afternoon_pct >= 35.0:
            rhythm = CodingRhythm.AFTERNOON_PEAK
        else:
            rhythm = CodingRhythm.BALANCED

        return rhythm, breakdown

    @classmethod
    def enrich_profile(cls, profile: DeveloperProfile) -> DeveloperProfile:
        """Enrich a developer profile with computed distributions, rhythm metrics and summary."""
        # 1. Update rhythm & hours breakdown
        rhythm, hours_breakdown = cls.compute_rhythm_profile(
            profile.night_owl_score, profile.weekend_activity_ratio
        )
        profile.coding_rhythm = rhythm
        profile.active_hours_breakdown = hours_breakdown

        # 2. Extract rich skill tags
        tags: Set[str] = set(profile.skill_tags)
        for stat in profile.top_languages:
            tags.add(stat.language)
        for repo in profile.featured_repos:
            for t in repo.topics:
                tags.add(t.replace("-", " ").title())
        profile.skill_tags = sorted(list(tags))[:10]

        # 3. Build AI synthesis if missing
        if not profile.ai_summary:
            top_langs = ", ".join([l.language for l in profile.top_languages[:3]]) or "Multiple languages"
            profile.ai_summary = (
                f"{profile.name or profile.username} is a {profile.experience_tier.value} specializing in {profile.primary_role.value}. "
                f"Most active with {top_langs}, operating with a {profile.coding_rhythm.value} rhythm."
            )

        return profile


profile_analyzer = ProfileAnalyzer()
