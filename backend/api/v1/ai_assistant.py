"""AI Assistant conversational endpoints for matchmaking and pairing guidance."""

from fastapi import APIRouter, HTTPException
from backend.models.collaboration import (
    AIChatRequest,
    AIChatResponse,
)
from backend.services.ai_assistant import ai_assistant_service

router = APIRouter()


@router.post("/chat", response_model=AIChatResponse)
async def chat_with_assistant(request: AIChatRequest):
    """Interact with DevOn AI Pair Assistant for advice, pitch refinement, and match insights."""
    try:
        return await ai_assistant_service.process_chat(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assistant error: {str(e)}")
