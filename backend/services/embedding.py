"""AI Semantic Embedding Vectorizer and Cosine Similarity Engine."""

import hashlib
import math
import re
from typing import Dict, List, Optional
import httpx
from backend.core.config import settings
from backend.models.developer import DeveloperProfile

# Vocabulary of key technical domains for semantic feature vector projection
VOCABULARY = [
    "python", "typescript", "javascript", "go", "rust", "c", "cpp", "csharp", "java", "ruby", "php",
    "html", "css", "react", "vue", "nextjs", "angular", "svelte", "tailwind", "design", "frontend",
    "fastapi", "django", "flask", "nodejs", "express", "backend", "api", "graphql", "rest", "microservices",
    "docker", "kubernetes", "terraform", "aws", "gcp", "azure", "ci", "cd", "devops", "cloud", "linux",
    "ai", "ml", "machinelearning", "deeplearning", "pytorch", "tensorflow", "rag", "agents", "llm", "nlp",
    "database", "postgresql", "mysql", "mongodb", "redis", "sqlite", "vector", "sql", "nosql",
    "mobile", "flutter", "reactnative", "swift", "kotlin", "ios", "android",
    "systems", "concurrency", "performance", "compiler", "wasm", "distributed", "security",
    "opensource", "git", "github", "testing", "architecture", "automation", "tools"
]
VOCAB_INDEX = {term: idx for idx, term in enumerate(VOCABULARY)}
DIMENSIONS = len(VOCABULARY)


class EmbeddingEngine:
    """Generates dense semantic vector embeddings for developer profiles and computes similarity."""

    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        self.openai_key = settings.OPENAI_API_KEY

    @staticmethod
    def extract_semantic_text(profile: DeveloperProfile) -> str:
        """Create rich semantic text representation of a developer profile."""
        languages_str = ", ".join([f"{l.language} ({l.percentage}%)" for l in profile.top_languages])
        tags_str = ", ".join(profile.skill_tags)
        domains_str = ", ".join(profile.domain_interests)
        repos_str = ", ".join([f"{r.name}: {r.description or ''}" for r in profile.featured_repos])

        return (
            f"Developer: {profile.name or profile.username}. "
            f"Role: {profile.primary_role.value}. Experience: {profile.experience_tier.value}. "
            f"Languages: {languages_str}. Skills: {tags_str}. "
            f"Domains: {domains_str}. Projects: {repos_str}. "
            f"Rhythm: {profile.coding_rhythm.value}. Bio: {profile.bio or ''}"
        )

    def vectorize_text(self, text: str) -> List[float]:
        """Convert text into normalized high-dimensional dense vector space."""
        # Tokenize and normalize words
        words = re.findall(r"\b[a-zA-Z0-9_\-\.\#\+]+\b", text.lower())
        vector = [0.0] * DIMENSIONS

        for word in words:
            clean_word = word.replace(".", "").replace("#", "sharp").replace("+", "p")
            if clean_word in VOCAB_INDEX:
                vector[VOCAB_INDEX[clean_word]] += 1.5
            else:
                # Deterministic hashed pseudo-embedding for unknown domain keywords
                h = int(hashlib.md5(clean_word.encode("utf-8")).hexdigest(), 16)
                idx = h % DIMENSIONS
                vector[idx] += 0.3

        # L2-normalize vector to unit length
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0:
            return [x / norm for x in vector]
        return vector

    async def get_profile_embedding(self, profile: DeveloperProfile) -> List[float]:
        """Compute embedding vector using Gemini API if key exists, or local vectorizer."""
        text = self.extract_semantic_text(profile)

        if self.gemini_key:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={self.gemini_key}"
                    res = await client.post(
                        url,
                        json={"model": "models/text-embedding-004", "content": {"parts": [{"text": text[:1000]}]}},
                    )
                    if res.status_code == 200:
                        values = res.json().get("embedding", {}).get("values", [])
                        if values:
                            return values
            except Exception:
                pass  # Fall back to local dense vectorizer

        return self.vectorize_text(text)

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Compute cosine similarity between two vectors (range 0.0 to 1.0)."""
        if not vec_a or not vec_b:
            return 0.5
        min_len = min(len(vec_a), len(vec_b))
        dot_product = sum(vec_a[i] * vec_b[i] for i in range(min_len))
        norm_a = math.sqrt(sum(x * x for x in vec_a[:min_len]))
        norm_b = math.sqrt(sum(x * x for x in vec_b[:min_len]))

        if norm_a == 0 or norm_b == 0:
            return 0.5

        similarity = dot_product / (norm_a * norm_b)
        # Clamp to [0.0, 1.0]
        return max(0.0, min(1.0, (similarity + 1.0) / 2.0 if similarity < 0 else similarity))


embedding_engine = EmbeddingEngine()
