"""Application configuration using Pydantic Settings."""

import os
from typing import List, Optional
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseSettings, ConfigDict as SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    """Application settings for DevOn."""

    PROJECT_NAME: str = "DevOn"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered developer matchmaker finding compatible coding partners using GitHub data analysis."
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # API Base URL & Prefixes
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:5500",
    ]

    # Security & Tokens
    SECRET_KEY: str = "devon-secret-super-secure-key-2026-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # GitHub OAuth & API
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"
    GITHUB_TOKEN: Optional[str] = None

    # AI & Embedding Providers
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-004"

    # Matchmaking Scoring Weights (total = 1.0)
    WEIGHT_SKILL_COMPLEMENTARITY: float = 0.40
    WEIGHT_SCHEDULE_COMPATIBILITY: float = 0.25
    WEIGHT_DOMAIN_INTERESTS: float = 0.20
    WEIGHT_EXPERIENCE_BALANCE: float = 0.15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
