"""GitHub OAuth 2.0 authentication endpoints."""

import urllib.parse
from typing import Optional
from fastapi import APIRouter, Cookie, HTTPException, Query, Response
from fastapi.responses import RedirectResponse
import httpx
from backend.core.config import settings
from backend.core.security import generate_session_token
from backend.models.developer import DeveloperProfile
from backend.services.github_client import github_client
from backend.services.analyzer import profile_analyzer

router = APIRouter()

# Active in-memory sessions: session_token -> username
_SESSIONS = {}


@router.get("/login")
async def github_login():
    """Redirect to GitHub OAuth consent screen."""
    if not settings.GITHUB_CLIENT_ID:
        # If OAuth keys not configured, redirect to demo mode
        return RedirectResponse(url="/?oauth_demo=true&user=SoroushSoleimani")

    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
        "scope": "read:user user:email",
        "state": generate_session_token(16),
    }
    github_url = f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url=github_url)


@router.get("/callback")
async def github_callback(
    code: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    response: Response = None,
):
    """Handle OAuth callback from GitHub and issue session token."""
    if error:
        raise HTTPException(status_code=400, detail=f"GitHub OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_url = "https://github.com/login/oauth/access_token"
    async with httpx.AsyncClient(timeout=10.0) as client:
        token_res = await client.post(
            token_url,
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )

        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve token from GitHub")

        token_data = token_res.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Access token missing in response")

        # Fetch authenticated user profile
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        )
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch GitHub profile")

        gh_user = user_res.json()
        username = gh_user.get("login")

        # Create session
        session_token = generate_session_token()
        _SESSIONS[session_token] = username

        redirect = RedirectResponse(url=f"/?auth_success=true&user={username}", status_code=302)
        redirect.set_cookie(
            key="devon_session",
            value=session_token,
            httponly=True,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return redirect


@router.get("/me", response_model=DeveloperProfile)
async def get_current_user(devon_session: Optional[str] = Cookie(None)):
    """Retrieve currently authenticated developer profile."""
    username = _SESSIONS.get(devon_session) if devon_session else None
    if not username:
        # Default to primary creator profile for instant demo experience
        username = "SoroushSoleimani"

    profile = await github_client.get_developer_profile(username)
    return profile_analyzer.enrich_profile(profile)


@router.post("/logout")
async def logout(response: Response, devon_session: Optional[str] = Cookie(None)):
    """Clear session and log out."""
    if devon_session and devon_session in _SESSIONS:
        del _SESSIONS[devon_session]
    response.delete_cookie("devon_session")
    return {"message": "Logged out successfully"}
