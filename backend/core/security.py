"""Security utilities: tokens, hashing, and request authentication."""

import hashlib
import hmac
import secrets
import time
from typing import Any, Dict, Optional
from backend.core.config import settings


def generate_session_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def hash_token(token: str) -> str:
    """Create a SHA-256 HMAC hash of a token using application SECRET_KEY."""
    return hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def verify_token_signature(token: str, expected_hash: str) -> bool:
    """Safely verify HMAC hash in constant time."""
    computed = hash_token(token)
    return hmac.compare_digest(computed, expected_hash)


def create_simple_jwt_payload(subject: str, custom_claims: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a standardized JWT-compatible session payload with expiry."""
    now = int(time.time())
    expire = now + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": expire,
    }
    if custom_claims:
        payload.update(custom_claims)
    return payload
