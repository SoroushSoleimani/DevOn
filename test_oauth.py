"""Standalone test script for validating GitHub OAuth 2.0 flow."""

import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
import httpx
from urllib.parse import quote
from dotenv import load_dotenv
from backend.core.config import settings

load_dotenv()

app = FastAPI(title="DevOn OAuth Standalone Verification")

CLIENT_ID = settings.GITHUB_CLIENT_ID or os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET or os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = settings.GITHUB_REDIRECT_URI or "http://localhost:8000/auth/github/callback"


def get_html_response(content: str, title: str = "DevOn OAuth") -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>{title}</title><meta charset="UTF-8"></head>
    <body style="font-family: sans-serif; padding: 20px; background: #0b0f19; color: #f8fafc;">
        <h2>{title}</h2>
        <pre style="background: #111827; padding: 16px; border-radius: 8px;">{content}</pre>
        <p><a href="/login" style="color: #38bdf8;">Login with GitHub</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/")
async def root():
    return get_html_response("Click below to test GitHub OAuth 2.0 flow.", "DevOn OAuth Standalone Verification")


@app.get("/login")
async def login():
    if not CLIENT_ID or not CLIENT_SECRET:
        return get_html_response("Notice: GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET are not set in .env. DevOn runs in demo mode.", "Demo Mode")
    github_auth_url = (
        "https://github.com/login/oauth/authorize?"
        f"client_id={CLIENT_ID}&redirect_uri={quote(REDIRECT_URI)}&scope=read:user,user:email"
    )
    return RedirectResponse(github_auth_url)


@app.get("/auth/github/callback")
async def callback(code: str = None, error: str = None):
    if error:
        return get_html_response(f"Error from GitHub: {error}", "OAuth Error")
    if not code:
        return get_html_response("Code parameter not found.", "OAuth Error")

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return get_html_response(f"Failed to get token: {token_data}", "OAuth Error")

        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()

        output = f"Login successful!\n\nUsername: {user_data.get('login')}\nName: {user_data.get('name')}\n"
        return get_html_response(output, "GitHub Profile")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)