import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
import httpx
from urllib.parse import quote
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

app = FastAPI(title="DevOn OAuth Test")

# Read values from environment
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/auth/github/callback")

# Simple validation
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET values not found in .env file")

def get_html_response(content: str, title: str = "DevOn OAuth") -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>{title}</title><meta charset="UTF-8"></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h2>{title}</h2>
        <pre>{content}</pre>
        <a href="/login">Login with GitHub</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/")
async def root():
    return get_html_response("Click the link below to test GitHub OAuth.", "DevOn OAuth Test")

@app.get("/login")
async def login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize?"
        f"client_id={CLIENT_ID}&redirect_uri={quote(REDIRECT_URI)}&scope=read:user,user:email"
    )
    return RedirectResponse(github_auth_url)

@app.get("/auth/github/login")
async def auth_github_login():
    return await login()

@app.get("/auth/github/callback")
async def callback(code: str = None, error: str = None):
    if error:
        return get_html_response(f"Error from GitHub: {error}", "Error")
    if not code:
        return get_html_response("Code parameter not found.", "Error")

    async with httpx.AsyncClient() as client:
        # Exchange code for token
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
            return get_html_response(f"Failed to get token: {token_data}", "Error")

        # Get user information
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()

        # Get emails
        emails_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        emails_data = emails_response.json()

        output = f"Login successful!\n\n"
        output += f"Username: {user_data.get('login')}\n"
        output += f"Name: {user_data.get('name')}\n"
        output += f"ID: {user_data.get('id')}\n"
        output += f"Public email: {user_data.get('email')}\n"
        output += f"All emails:\n{emails_data}\n\n"
        output += f"Full user info:\n{user_data}"

        return get_html_response(output, "GitHub Profile")