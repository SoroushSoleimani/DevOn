"""Matchmaking Engine: multi-factor compatibility scoring and partner recommendations."""

import math
from typing import List, Optional, Set, Tuple
from backend.core.config import settings
from backend.models.developer import (
    DeveloperProfile,
    PrimaryRole,
    ExperienceTier,
    CodingRhythm,
)
from backend.models.matching import (
    MatchResult,
    MatchFilter,
    CompatibilityBreakdown,
    DeveloperComparison,
    PairingMode,
)
from backend.services.analyzer import profile_analyzer
from backend.services.embedding import embedding_engine
from backend.services.github_client import github_client

# Synergy scores for complementary pairing mode
ROLE_COMPLEMENTARITY_MATRIX = {
    (PrimaryRole.BACKEND, PrimaryRole.FRONTEND): 96.0,
    (PrimaryRole.FRONTEND, PrimaryRole.BACKEND): 96.0,
    (PrimaryRole.AIML, PrimaryRole.BACKEND): 92.0,
    (PrimaryRole.BACKEND, PrimaryRole.AIML): 92.0,
    (PrimaryRole.AIML, PrimaryRole.FRONTEND): 88.0,
    (PrimaryRole.FRONTEND, PrimaryRole.AIML): 88.0,
    (PrimaryRole.BACKEND, PrimaryRole.DEVOPS): 94.0,
    (PrimaryRole.DEVOPS, PrimaryRole.BACKEND): 94.0,
    (PrimaryRole.BACKEND, PrimaryRole.MOBILE): 90.0,
    (PrimaryRole.MOBILE, PrimaryRole.BACKEND): 90.0,
    (PrimaryRole.SYSTEMS, PrimaryRole.BACKEND): 86.0,
    (PrimaryRole.BACKEND, PrimaryRole.SYSTEMS): 86.0,
    (PrimaryRole.FULLSTACK, PrimaryRole.FRONTEND): 85.0,
    (PrimaryRole.FULLSTACK, PrimaryRole.BACKEND): 85.0,
    (PrimaryRole.FULLSTACK, PrimaryRole.AIML): 87.0,
    (PrimaryRole.FULLSTACK, PrimaryRole.DEVOPS): 89.0,
}


class MatchmakerEngine:
    """Computes multidimensional developer compatibility scores."""

    @staticmethod
    def calculate_skill_score(
        dev_a: DeveloperProfile, dev_b: DeveloperProfile, mode: PairingMode
    ) -> Tuple[float, List[str], List[str]]:
        """Calculate skill compatibility, complementary skill pairs, and shared skills."""
        tags_a: Set[str] = set([t.lower() for t in dev_a.skill_tags])
        tags_b: Set[str] = set([t.lower() for t in dev_b.skill_tags])

        shared_tags = [t.title() for t in tags_a.intersection(tags_b)]
        diff_a = [t.title() for t in tags_a - tags_b][:3]
        diff_b = [t.title() for t in tags_b - tags_a][:3]
        complementary = [f"{a} + {b}" for a, b in zip(diff_a, diff_b)]

        if mode == PairingMode.SIMILAR:
            # Reward identical roles and maximum skill overlap
            if dev_a.primary_role == dev_b.primary_role:
                base_score = 85.0
            else:
                base_score = 55.0
            overlap_ratio = len(shared_tags) / max(1, len(tags_a.union(tags_b)))
            score = base_score + (overlap_ratio * 15.0)
        else:
            # Complementary mode: reward cross-disciplinary strengths
            key = (dev_a.primary_role, dev_b.primary_role)
            score = ROLE_COMPLEMENTARITY_MATRIX.get(key, 78.0)
            if shared_tags:
                score = min(99.0, score + 4.0)  # bonus for having a common ground language

        return round(score, 1), complementary, shared_tags

    @staticmethod
    def calculate_schedule_score(
        dev_a: DeveloperProfile, dev_b: DeveloperProfile
    ) -> Tuple[float, List[str]]:
        """Calculate work rhythm and timezone compatibility score."""
        reasons = []

        # 1. Night owl / Early bird alignment (0.0 to 1.0 diff)
        rhythm_diff = abs(dev_a.night_owl_score - dev_b.night_owl_score)
        rhythm_score = max(40.0, 100.0 - (rhythm_diff * 60.0))

        if rhythm_diff <= 0.2:
            reasons.append(f"Synchronized coding rhythm: both enjoy {dev_a.coding_rhythm.value}")
        elif rhythm_diff >= 0.5:
            reasons.append(f"Complementary schedules: {dev_a.coding_rhythm.value} and {dev_b.coding_rhythm.value}")

        # 2. Timezone difference
        tz_diff = abs(dev_a.timezone_offset_hours - dev_b.timezone_offset_hours)
        if tz_diff <= 2.0:
            tz_score = 100.0
            reasons.append(f"Near-identical timezones (under {tz_diff}h offset)")
        elif tz_diff <= 5.0:
            tz_score = 82.0
            reasons.append(f"Workable timezone overlap ({tz_diff}h difference)")
        elif tz_diff <= 8.0:
            tz_score = 65.0
        else:
            tz_score = 45.0

        # Weighted combination
        schedule_score = (rhythm_score * 0.6) + (tz_score * 0.4)
        return round(schedule_score, 1), reasons

    @staticmethod
    def calculate_domain_score(
        dev_a: DeveloperProfile, dev_b: DeveloperProfile
    ) -> Tuple[float, List[str]]:
        """Calculate domain and project interests overlap."""
        interests_a = set([i.lower() for i in dev_a.domain_interests])
        interests_b = set([i.lower() for i in dev_b.domain_interests])

        shared = [i.title() for i in interests_a.intersection(interests_b)]
        if not shared:
            # Fall back to general overlap
            return 60.0, ["Open Source Exploration"]

        jaccard = len(shared) / max(1, len(interests_a.union(interests_b)))
        score = 65.0 + (jaccard * 35.0)
        return round(min(98.0, score), 1), shared

    @staticmethod
    def calculate_experience_score(
        dev_a: DeveloperProfile, dev_b: DeveloperProfile, mode: PairingMode
    ) -> float:
        """Calculate experience synergy based on pairing strategy."""
        tier_weights = {
            ExperienceTier.BEGINNER: 1,
            ExperienceTier.INTERMEDIATE: 2,
            ExperienceTier.SENIOR: 3,
            ExperienceTier.STAFF: 4,
        }
        w_a = tier_weights.get(dev_a.experience_tier, 2)
        w_b = tier_weights.get(dev_b.experience_tier, 2)
        diff = abs(w_a - w_b)

        if mode == PairingMode.MENTORSHIP:
            return 95.0 if diff >= 1 else 70.0
        elif mode == PairingMode.PEER_LEARNING:
            return 95.0 if diff == 0 else max(60.0, 90.0 - (diff * 15.0))
        else:
            # Balanced: slight differences provide great mutual learning
            return 92.0 if diff <= 1 else 78.0

    async def evaluate_pair(
        self, dev_a: DeveloperProfile, dev_b: DeveloperProfile, mode: PairingMode = PairingMode.COMPLEMENTARY
    ) -> MatchResult:
        """Evaluate full compatibility breakdown between two developers."""
        # 1. Skill score
        skill_score, complementary, shared_skills = self.calculate_skill_score(dev_a, dev_b, mode)

        # 2. Schedule score
        schedule_score, sched_reasons = self.calculate_schedule_score(dev_a, dev_b)

        # 3. Domain score
        domain_score, shared_interests = self.calculate_domain_score(dev_a, dev_b)

        # 4. Experience score
        experience_score = self.calculate_experience_score(dev_a, dev_b, mode)

        # 5. Semantic Vector similarity
        vec_a = await embedding_engine.get_profile_embedding(dev_a)
        vec_b = await embedding_engine.get_profile_embedding(dev_b)
        vector_sim = embedding_engine.cosine_similarity(vec_a, vec_b) * 100.0

        breakdown = CompatibilityBreakdown(
            skill_complementarity=skill_score,
            schedule_compatibility=schedule_score,
            domain_interests_overlap=domain_score,
            experience_tier_synergy=experience_score,
            semantic_vector_similarity=round(vector_sim, 1),
        )

        # Overall weighted score
        overall = (
            (skill_score * settings.WEIGHT_SKILL_COMPLEMENTARITY)
            + (schedule_score * settings.WEIGHT_SCHEDULE_COMPATIBILITY)
            + (domain_score * settings.WEIGHT_DOMAIN_INTERESTS)
            + (experience_score * settings.WEIGHT_EXPERIENCE_BALANCE)
        )
        overall = round(max(30.0, min(99.0, overall)), 1)

        # Build synergy highlights
        synergy_reasons = []
        if mode == PairingMode.COMPLEMENTARY:
            synergy_reasons.append(
                f"Full-stack superpower: {dev_a.primary_role.value} pairs perfectly with {dev_b.primary_role.value}"
            )
        else:
            synergy_reasons.append(f"Deep shared mastery in {dev_a.primary_role.value}")

        synergy_reasons.extend(sched_reasons[:2])
        if shared_interests:
            synergy_reasons.append(f"Shared passion for {', '.join(shared_interests[:2])}")

        potential_topics = [
            f"Build a {dev_a.primary_role.name.lower()}-{dev_b.primary_role.name.lower()} end-to-end prototype",
            f"Collaborate on open source issues in {shared_skills[0] if shared_skills else 'software architecture'}",
            "Conduct mutual code reviews and pair-debug complex modules",
        ]

        return MatchResult(
            developer=dev_b,
            overall_score=overall,
            breakdown=breakdown,
            pairing_mode=mode,
            synergy_reasons=synergy_reasons,
            shared_interests=shared_interests,
            complementary_skills=complementary,
            potential_collaboration_topics=potential_topics,
        )

    async def find_matches_for_user(
        self, username: str, match_filter: Optional[MatchFilter] = None
    ) -> List[MatchResult]:
        """Find best partner matches for a user from community profiles."""
        filter_cfg = match_filter or MatchFilter()
        user_profile = await github_client.get_developer_profile(username)
        user_profile = profile_analyzer.enrich_profile(user_profile)

        candidates = await github_client.list_community_developers()
        results: List[MatchResult] = []

        for candidate in candidates:
            # Don't match user with themselves
            if candidate.username.lower() == user_profile.username.lower():
                continue

            # Apply hard filters if specified
            if filter_cfg.primary_role and candidate.primary_role != filter_cfg.primary_role:
                continue
            if filter_cfg.experience_tier and candidate.experience_tier != filter_cfg.experience_tier:
                continue
            if filter_cfg.coding_rhythm and candidate.coding_rhythm != filter_cfg.coding_rhythm:
                continue
            if filter_cfg.target_language:
                cand_langs = [l.language.lower() for l in candidate.top_languages]
                if filter_cfg.target_language.lower() not in cand_langs:
                    continue

            # Evaluate compatibility
            result = await self.evaluate_pair(user_profile, candidate, filter_cfg.pairing_mode)
            if result.overall_score >= filter_cfg.min_compatibility_score:
                results.append(result)

        # Sort descending by overall compatibility score
        results.sort(key=lambda r: r.overall_score, reverse=True)
        return results[: filter_cfg.limit]

    async def compare_developers(self, username_a: str, username_b: str) -> DeveloperComparison:
        """Perform side-by-side comparison between two developers."""
        dev_a = await github_client.get_developer_profile(username_a)
        dev_b = await github_client.get_developer_profile(username_b)
        dev_a = profile_analyzer.enrich_profile(dev_a)
        dev_b = profile_analyzer.enrich_profile(dev_b)

        result = await self.evaluate_pair(dev_a, dev_b, PairingMode.COMPLEMENTARY)

        frictions = []
        tz_diff = abs(dev_a.timezone_offset_hours - dev_b.timezone_offset_hours)
        if tz_diff > 6.0:
            frictions.append(f"Significant timezone gap ({tz_diff}h offset) - asynchronous communication recommended.")
        if abs(dev_a.night_owl_score - dev_b.night_owl_score) > 0.5:
            frictions.append("Different peak hours (night owl vs morning lark) - set explicit sync windows.")

        return DeveloperComparison(
            developer_a=dev_a,
            developer_b=dev_b,
            overall_compatibility=result.overall_score,
            breakdown=result.breakdown,
            synergy_highlights=result.synergy_reasons,
            potential_friction_points=frictions,
            suggested_focus=f"Kickstart pair session around {dev_a.primary_role.value} and {dev_b.primary_role.value} integration.",
        )


matchmaker_engine = MatchmakerEngine()
