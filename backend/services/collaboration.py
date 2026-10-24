"""Collaboration idea generator and outreach pitch synthesizer."""

from typing import List
from backend.models.developer import DeveloperProfile, PrimaryRole
from backend.models.collaboration import (
    PairProjectIdea,
    CollaborationPitch,
    RecommendedIssue,
)


class CollaborationService:
    """Generates pair programming project concepts, issues, and icebreakers."""

    @staticmethod
    def generate_project_ideas(dev_a: DeveloperProfile, dev_b: DeveloperProfile) -> List[PairProjectIdea]:
        """Synthesize concrete pair programming projects tailored to the two developers."""
        role_a = dev_a.primary_role
        role_b = dev_b.primary_role
        top_lang_a = dev_a.top_languages[0].language if dev_a.top_languages else "Python"
        top_lang_b = dev_b.top_languages[0].language if dev_b.top_languages else "TypeScript"

        ideas: List[PairProjectIdea] = []

        # Project 1: Cross-Domain Fullstack application
        ideas.append(
            PairProjectIdea(
                title=f"AI-Powered {top_lang_a} & {top_lang_b} Collaborative Studio",
                description=(
                    f"An intelligent developer workspace combining a high-performance {top_lang_a} backend "
                    f"with a responsive {top_lang_b} frontend client, integrating real-time agent workflows."
                ),
                recommended_tech_stack=[top_lang_a, top_lang_b, "FastAPI", "WebSockets", "Docker"],
                developer_a_role=f"{dev_a.name or dev_a.username}: Core Engine & Data Pipelines ({role_a.value})",
                developer_b_role=f"{dev_b.name or dev_b.username}: Client Interface & UX Flow ({role_b.value})",
                estimated_difficulty="Intermediate",
                why_good_fit=(
                    f"Leverages {dev_a.username}'s experience in {role_a.value} alongside "
                    f"{dev_b.username}'s strengths in {role_b.value} for an end-to-end synergy."
                ),
            )
        )

        # Project 2: Open Source Tooling / CLI / Microservice
        ideas.append(
            PairProjectIdea(
                title=f"Autonomous GitHub Action for {dev_a.domain_interests[0] if dev_a.domain_interests else 'CI/CD'}",
                description=(
                    "A community GitHub Action that analyzes repository PRs, detects anti-patterns, "
                    "and suggests optimizations with interactive preview badges."
                ),
                recommended_tech_stack=[top_lang_a, "GitHub Actions", "Docker", "REST API"],
                developer_a_role=f"{dev_a.name or dev_a.username}: Core logic & API bindings",
                developer_b_role=f"{dev_b.name or dev_b.username}: Integration tests & Documentation",
                estimated_difficulty="Beginner to Intermediate",
                why_good_fit="Quick 1-2 weekend turnaround that creates an immediate portfolio artifact for both.",
            )
        )

        return ideas

    @classmethod
    def generate_collaboration_pitch(
        cls, dev_a: DeveloperProfile, dev_b: DeveloperProfile
    ) -> CollaborationPitch:
        """Create a polite, high-converting outreach message and icebreaker."""
        ideas = cls.generate_project_ideas(dev_a, dev_b)
        best_idea = ideas[0]

        top_lang_a = dev_a.top_languages[0].language if dev_a.top_languages else "Python"
        top_lang_b = dev_b.top_languages[0].language if dev_b.top_languages else "TypeScript"

        pitch_text = (
            f"Hey {dev_b.name or dev_b.username}! 👋\n\n"
            f"I came across your profile through DevOn and was really impressed by your work in {dev_b.primary_role.value} "
            f"and projects like '{dev_b.featured_repos[0].name if dev_b.featured_repos else top_lang_b}'.\n\n"
            f"I focus primarily on {dev_a.primary_role.value} with {top_lang_a}. DevOn highlighted that our skills have "
            f"strong complementary synergy. I had an idea for a collaborative project: '{best_idea.title}'.\n\n"
            f"Would you be open to a 20-minute chat or an asynchronous GitHub repo brainstorm to see if we'd enjoy pairing up?"
        )

        slots = [
            f"Weekday evenings ({dev_a.coding_rhythm.value} sync window)",
            "Weekend hackathon sprint (2 hours)",
            "Async GitHub Discussion & PR reviews",
        ]

        return CollaborationPitch(
            developer_a_username=dev_a.username,
            developer_b_username=dev_b.username,
            icebreaker_text=pitch_text,
            pitch_subject=f"Pair Programming collaboration on {best_idea.title} via DevOn",
            suggested_project_ideas=ideas,
            recommended_schedule_slots=slots,
        )


collaboration_service = CollaborationService()
