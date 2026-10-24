"""AI Assistant service for developer matchmaking Q&A and onboarding."""

import logging
from typing import List, Optional
import httpx
from backend.core.config import settings
from backend.models.collaboration import (
    AIChatMessage,
    AIChatRequest,
    AIChatResponse,
)
from backend.services.github_client import github_client
from backend.services.matchmaker import matchmaker_engine

logger = logging.getLogger(__name__)


class AIAssistantService:
    """Provides conversational advice and matchmaking insights."""

    @staticmethod
    async def process_chat(request: AIChatRequest) -> AIChatResponse:
        """Process chat message regarding developer matching and collaboration."""
        user_msg = request.messages[-1].content.lower() if request.messages else ""
        dev_a = await github_client.get_developer_profile(request.developer_username)

        # Candidate profile if specified
        dev_b = None
        if request.candidate_username:
            dev_b = await github_client.get_developer_profile(request.candidate_username)

        # Context-aware intelligent responses
        if "icebreaker" in user_msg or "pitch" in user_msg or "message" in user_msg:
            candidate_name = dev_b.name if dev_b else "your match"
            reply = (
                f"Here's an effective outreach icebreaker for {candidate_name}:\n\n"
                f"\"Hi {candidate_name}! I saw on DevOn that we have great complementary skills. "
                f"I'm working on backend APIs with {dev_a.top_languages[0].language if dev_a.top_languages else 'Python'}, "
                f"and I'd love to connect on building a lightweight open-source tool together. Are you open to pairing up?\""
            )
            actions = ["Copy pitch to clipboard", "Customize project idea", "View schedule overlap"]

        elif "schedule" in user_msg or "timezone" in user_msg or "time" in user_msg:
            if dev_b:
                tz_diff = abs(dev_a.timezone_offset_hours - dev_b.timezone_offset_hours)
                reply = (
                    f"Schedule analysis between {dev_a.username} and {dev_b.username}:\n"
                    f"- Timezone Difference: {tz_diff} hours\n"
                    f"- {dev_a.username} Rhythm: {dev_a.coding_rhythm.value}\n"
                    f"- {dev_b.username} Rhythm: {dev_b.coding_rhythm.value}\n\n"
                    f"💡 Tip: If you have more than 4 hours difference, focus on async PR reviews "
                    f"with a single 30-minute weekly live sync."
                )
            else:
                reply = f"Your rhythm is {dev_a.coding_rhythm.value}. We prioritize partners active during your peak hours."
            actions = ["Find matches in same timezone", "Adjust rhythm filter", "View schedule breakdown"]

        elif "project" in user_msg or "idea" in user_msg:
            reply = (
                f"Top project recommendation for your skillset ({dev_a.primary_role.value}):\n"
                f"1. **Fullstack Agentic Workflow Playground**: Python FastAPI backend with reactive TypeScript UI.\n"
                f"2. **Real-time Developer Analytics Dashboard**: WebSocket streaming of GitHub telemetry.\n"
                f"3. **Modular CLI Developer Hub**: Lightweight Rust or Go tool integrating with DevOn API."
            )
            actions = ["Generate collaboration pitch", "Browse similar repos", "Start repo setup"]

        else:
            reply = (
                f"Hello {dev_a.name or dev_a.username}! I am your DevOn Pair Assistant. "
                f"I can help you analyze partner compatibility, craft personalized outreach icebreakers, "
                f"or design custom pair programming projects tailored to your tech stack. What would you like to explore?"
            )
            actions = ["Find top matches", "Generate collaboration pitch", "Compare two developers"]

        return AIChatResponse(reply=reply, suggested_actions=actions)


ai_assistant_service = AIAssistantService()
