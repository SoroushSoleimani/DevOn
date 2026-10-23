"""GitHub API Client with async HTTPX, caching, and resilient fallback data."""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional
import httpx
from backend.core.config import settings
from backend.models.developer import (
    DeveloperProfile,
    LanguageStat,
    RepositorySummary,
    PrimaryRole,
    ExperienceTier,
    CodingRhythm,
)

logger = logging.getLogger(__name__)

# In-memory profile cache with TTL
_CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_SECONDS = 3600  # 1 hour


# Curated high-fidelity developer profiles for instant demo and offline fallback
SEED_DEVELOPERS: Dict[str, Dict[str, Any]] = {
    "SoroushSoleimani": {
        "username": "SoroushSoleimani",
        "name": "Soroush Soleimani",
        "avatar_url": "https://avatars.githubusercontent.com/u/140951703?v=4",
        "bio": "AI & Full-Stack Developer | Building autonomous systems & collaborative dev tools.",
        "company": "Independent / Open Source",
        "location": "Tehran, Iran",
        "timezone_offset_hours": 3.5,
        "public_repos_count": 18,
        "total_stars_received": 42,
        "followers_count": 34,
        "following_count": 28,
        "primary_role": PrimaryRole.BACKEND,
        "experience_tier": ExperienceTier.SENIOR,
        "coding_rhythm": CodingRhythm.NIGHT_OWL,
        "night_owl_score": 0.85,
        "weekend_activity_ratio": 0.38,
        "top_languages": [
            {"language": "Python", "bytes_count": 450000, "percentage": 52.0, "repo_count": 10},
            {"language": "TypeScript", "bytes_count": 210000, "percentage": 24.0, "repo_count": 4},
            {"language": "JavaScript", "bytes_count": 120000, "percentage": 14.0, "repo_count": 3},
            {"language": "C++", "bytes_count": 85000, "percentage": 10.0, "repo_count": 2},
        ],
        "skill_tags": ["FastAPI", "Python", "Docker", "PyTorch", "AsyncIO", "PostgreSQL", "Next.js"],
        "domain_interests": ["AI Agents", "Developer Tools", "Distributed Systems", "Pair Programming"],
        "featured_repos": [
            {
                "name": "DevOn",
                "description": "AI-powered developer matchmaker finding compatible coding partners using GitHub data analysis.",
                "html_url": "https://github.com/SoroushSoleimani/DevOn",
                "language": "Python",
                "stargazers_count": 15,
                "forks_count": 3,
                "topics": ["ai-matchmaker", "fastapi", "github-api", "pair-programming"],
            },
            {
                "name": "autonomous-agent-core",
                "description": "Lightweight autonomous agent runtime with memory and tool calling.",
                "html_url": "https://github.com/SoroushSoleimani/autonomous-agent-core",
                "language": "Python",
                "stargazers_count": 19,
                "forks_count": 4,
                "topics": ["agents", "llm", "automation"],
            },
        ],
        "ai_summary": "High-velocity backend and AI developer specializing in asynchronous architectures, agentic workflows, and FastAPI platforms. Thrives during night hours with strong architectural design skills.",
    },
    "elena-codes": {
        "username": "elena-codes",
        "name": "Elena Rostova",
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face",
        "bio": "Frontend Architect & Design Systems Lead. Passionate about glassmorphism, micro-interactions and accessibility.",
        "company": "Voxel UI",
        "location": "Berlin, Germany",
        "timezone_offset_hours": 1.0,
        "public_repos_count": 24,
        "total_stars_received": 148,
        "followers_count": 112,
        "following_count": 45,
        "primary_role": PrimaryRole.FRONTEND,
        "experience_tier": ExperienceTier.SENIOR,
        "coding_rhythm": CodingRhythm.BALANCED,
        "night_owl_score": 0.40,
        "weekend_activity_ratio": 0.22,
        "top_languages": [
            {"language": "TypeScript", "bytes_count": 520000, "percentage": 58.0, "repo_count": 12},
            {"language": "CSS", "bytes_count": 220000, "percentage": 25.0, "repo_count": 7},
            {"language": "JavaScript", "bytes_count": 110000, "percentage": 12.0, "repo_count": 4},
            {"language": "HTML", "bytes_count": 45000, "percentage": 5.0, "repo_count": 3},
        ],
        "skill_tags": ["React", "TypeScript", "TailwindCSS", "Design Systems", "Web Audio", "Vite", "Zustand"],
        "domain_interests": ["Design Systems", "Developer Tools", "Data Visualization", "Creative Coding"],
        "featured_repos": [
            {
                "name": "fluid-design-tokens",
                "description": "Zero-runtime CSS token compiler for reactive design systems.",
                "html_url": "https://github.com/elena-codes/fluid-design-tokens",
                "language": "TypeScript",
                "stargazers_count": 89,
                "forks_count": 14,
                "topics": ["design-systems", "css", "tokens"],
            }
        ],
        "ai_summary": "Frontend specialist who crafts pixel-perfect, accessible user interfaces. Ideal counterpart for backend-heavy developers to build polished full-stack applications.",
    },
    "marcus-devops": {
        "username": "marcus-devops",
        "name": "Marcus Vance",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
        "bio": "Kubernetes whisperer, Terraform addict, and CI/CD pipeline architect. Observability evangelist.",
        "company": "CloudNative Labs",
        "location": "Austin, TX, USA",
        "timezone_offset_hours": -6.0,
        "public_repos_count": 31,
        "total_stars_received": 210,
        "followers_count": 89,
        "following_count": 52,
        "primary_role": PrimaryRole.DEVOPS,
        "experience_tier": ExperienceTier.STAFF,
        "coding_rhythm": CodingRhythm.EARLY_BIRD,
        "night_owl_score": 0.15,
        "weekend_activity_ratio": 0.15,
        "top_languages": [
            {"language": "Go", "bytes_count": 410000, "percentage": 48.0, "repo_count": 11},
            {"language": "HCL", "bytes_count": 220000, "percentage": 26.0, "repo_count": 8},
            {"language": "Python", "bytes_count": 150000, "percentage": 18.0, "repo_count": 6},
            {"language": "Shell", "bytes_count": 70000, "percentage": 8.0, "repo_count": 5},
        ],
        "skill_tags": ["Kubernetes", "Docker", "Terraform", "Go", "Prometheus", "CI/CD", "AWS"],
        "domain_interests": ["Cloud Infrastructure", "Distributed Systems", "Developer Tools", "Security"],
        "featured_repos": [
            {
                "name": "k8s-autoscale-operator",
                "description": "Predictive autoscaling custom controller for Kubernetes workloads.",
                "html_url": "https://github.com/marcus-devops/k8s-autoscale-operator",
                "language": "Go",
                "stargazers_count": 132,
                "forks_count": 28,
                "topics": ["kubernetes", "golang", "operator"],
            }
        ],
        "ai_summary": "Senior cloud and infrastructure engineer who excels at container orchestration and scalable pipelines. Early bird who loves pairing on robust production readiness.",
    },
    "priya-ai": {
        "username": "priya-ai",
        "name": "Priya Sharma",
        "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&h=150&fit=crop&crop=face",
        "bio": "ML Researcher & GenAI Engineer. Exploring retrieval-augmented generation and vector index optimization.",
        "company": "DeepData AI",
        "location": "Toronto, Canada",
        "timezone_offset_hours": -5.0,
        "public_repos_count": 16,
        "total_stars_received": 95,
        "followers_count": 76,
        "following_count": 60,
        "primary_role": PrimaryRole.AIML,
        "experience_tier": ExperienceTier.SENIOR,
        "coding_rhythm": CodingRhythm.NIGHT_OWL,
        "night_owl_score": 0.78,
        "weekend_activity_ratio": 0.35,
        "top_languages": [
            {"language": "Python", "bytes_count": 580000, "percentage": 75.0, "repo_count": 10},
            {"language": "Jupyter Notebook", "bytes_count": 120000, "percentage": 15.0, "repo_count": 4},
            {"language": "Rust", "bytes_count": 80000, "percentage": 10.0, "repo_count": 2},
        ],
        "skill_tags": ["PyTorch", "HuggingFace", "Python", "RAG", "FAISS", "LangChain", "FastAPI"],
        "domain_interests": ["AI Agents", "LLMs", "Vector Databases", "Information Retrieval"],
        "featured_repos": [
            {
                "name": "rag-eval-suite",
                "description": "Benchmarking and evaluation harness for multi-hop RAG pipelines.",
                "html_url": "https://github.com/priya-ai/rag-eval-suite",
                "language": "Python",
                "stargazers_count": 64,
                "forks_count": 11,
                "topics": ["rag", "llm-eval", "pytorch"],
            }
        ],
        "ai_summary": "Machine learning practitioner passionate about cutting-edge LLMs and vector search. Excellent collaborator for AI-driven applications and agent tools.",
    },
    "kenji-mobile": {
        "username": "kenji-mobile",
        "name": "Kenji Takahashi",
        "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
        "bio": "Cross-platform mobile developer (Flutter & Kotlin Multiplatform). Obsessed with 120fps animations.",
        "company": "AppCraft",
        "location": "Tokyo, Japan",
        "timezone_offset_hours": 9.0,
        "public_repos_count": 20,
        "total_stars_received": 88,
        "followers_count": 55,
        "following_count": 40,
        "primary_role": PrimaryRole.MOBILE,
        "experience_tier": ExperienceTier.INTERMEDIATE,
        "coding_rhythm": CodingRhythm.WEEKEND_WARRIOR,
        "night_owl_score": 0.60,
        "weekend_activity_ratio": 0.50,
        "top_languages": [
            {"language": "Dart", "bytes_count": 390000, "percentage": 50.0, "repo_count": 8},
            {"language": "Kotlin", "bytes_count": 230000, "percentage": 30.0, "repo_count": 6},
            {"language": "Swift", "bytes_count": 150000, "percentage": 20.0, "repo_count": 4},
        ],
        "skill_tags": ["Flutter", "Dart", "Kotlin", "Swift", "Mobile UX", "SQLite", "Firebase"],
        "domain_interests": ["Mobile Apps", "UI Animation", "Offline-first", "Open Source"],
        "featured_repos": [
            {
                "name": "smooth-flutter-animations",
                "description": "Custom high-performance physics-based transition controllers for Flutter.",
                "html_url": "https://github.com/kenji-mobile/smooth-flutter-animations",
                "language": "Dart",
                "stargazers_count": 58,
                "forks_count": 9,
                "topics": ["flutter", "animations", "mobile"],
            }
        ],
        "ai_summary": "Mobile client expert building fluid cross-platform experiences. Great pair for backend engineers wanting to bring APIs to iOS and Android.",
    },
    "alex-systems": {
        "username": "alex-systems",
        "name": "Alex Mercer",
        "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&h=150&fit=crop&crop=face",
        "bio": "Low-level hacker, Rustacean, and database engine enthusiast. Zero-cost abstractions only.",
        "company": "KernelByte",
        "location": "Stockholm, Sweden",
        "timezone_offset_hours": 1.0,
        "public_repos_count": 28,
        "total_stars_received": 340,
        "followers_count": 190,
        "following_count": 35,
        "primary_role": PrimaryRole.SYSTEMS,
        "experience_tier": ExperienceTier.SENIOR,
        "coding_rhythm": CodingRhythm.NIGHT_OWL,
        "night_owl_score": 0.72,
        "weekend_activity_ratio": 0.30,
        "top_languages": [
            {"language": "Rust", "bytes_count": 620000, "percentage": 70.0, "repo_count": 14},
            {"language": "C", "bytes_count": 180000, "percentage": 20.0, "repo_count": 5},
            {"language": "Python", "bytes_count": 90000, "percentage": 10.0, "repo_count": 4},
        ],
        "skill_tags": ["Rust", "Systems Programming", "Concurrency", "Linux", "Memory Safety", "WASM"],
        "domain_interests": ["Database Engines", "Distributed Systems", "Compilers", "WebAssembly"],
        "featured_repos": [
            {
                "name": "tiny-lsm-tree",
                "description": "Log-structured merge-tree key-value store implemented in pure safe Rust.",
                "html_url": "https://github.com/alex-systems/tiny-lsm-tree",
                "language": "Rust",
                "stargazers_count": 240,
                "forks_count": 35,
                "topics": ["rust", "database", "storage-engine"],
            }
        ],
        "ai_summary": "High-caliber systems engineer focusing on performance, memory safety, and concurrency. Loves pairing on demanding backend cores and WASM runtimes.",
    },
}


class GitHubClient:
    """Async client for GitHub REST API with caching and resilient fallback."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "DevOn-Matchmaker/1.0",
        }
        if self.token and self.token.startswith("gh"):
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_raw_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Fetch raw user JSON from GitHub API."""
        url = f"{self.base_url}/users/{username}"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(url, headers=self._get_headers())
                if res.status_code == 200:
                    return res.json()
                elif res.status_code == 404:
                    logger.warning("User %s not found on GitHub", username)
                    return None
                else:
                    logger.warning("GitHub API returned status %s for user %s", res.status_code, username)
                    return None
        except Exception as e:
            logger.error("Error connecting to GitHub for %s: %s", username, e)
            return None

    async def get_raw_repos(self, username: str, limit: int = 30) -> List[Dict[str, Any]]:
        """Fetch public repositories for a user."""
        url = f"{self.base_url}/users/{username}/repos?per_page={limit}&sort=updated"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(url, headers=self._get_headers())
                if res.status_code == 200:
                    return res.json()
                return []
        except Exception as e:
            logger.error("Error fetching repos for %s: %s", username, e)
            return []

    async def get_developer_profile(self, username: str) -> DeveloperProfile:
        """Fetch and synthesize developer profile with caching and fallback support."""
        # 1. Check cache
        cached = _CACHE.get(username.lower())
        if cached and (time.time() - cached["cached_at"] < CACHE_TTL_SECONDS):
            return cached["profile"]

        # 2. Try fetching live GitHub data
        raw_user = await self.get_raw_user(username)
        raw_repos = await self.get_raw_repos(username) if raw_user else []

        if raw_user:
            # Construct live profile
            profile = self._build_profile_from_live_data(raw_user, raw_repos)
        elif username in SEED_DEVELOPERS:
            # Fallback to seed profile
            profile = DeveloperProfile(**SEED_DEVELOPERS[username])
        elif username.lower() in [k.lower() for k in SEED_DEVELOPERS]:
            matching_key = next(k for k in SEED_DEVELOPERS if k.lower() == username.lower())
            profile = DeveloperProfile(**SEED_DEVELOPERS[matching_key])
        else:
            # Synthesize generic developer profile
            profile = self._build_synthetic_profile(username)

        # Cache result
        _CACHE[username.lower()] = {
            "profile": profile,
            "cached_at": time.time(),
        }
        return profile

    def _build_profile_from_live_data(
        self, user_data: Dict[str, Any], repos_data: List[Dict[str, Any]]
    ) -> DeveloperProfile:
        """Analyze raw GitHub API response into standard DeveloperProfile."""
        # Aggregate languages
        lang_counts: Dict[str, int] = {}
        total_stars = 0
        featured_repos: List[RepositorySummary] = []

        for repo in repos_data:
            lang = repo.get("language")
            stars = repo.get("stargazers_count", 0)
            total_stars += stars
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

            if len(featured_repos) < 5 and not repo.get("fork"):
                featured_repos.append(
                    RepositorySummary(
                        name=repo.get("name", ""),
                        description=repo.get("description"),
                        html_url=repo.get("html_url", ""),
                        language=lang,
                        stargazers_count=stars,
                        forks_count=repo.get("forks_count", 0),
                        topics=repo.get("topics", []),
                        is_fork=repo.get("fork", False),
                        updated_at=repo.get("updated_at"),
                    )
                )

        total_lang_instances = sum(lang_counts.values()) or 1
        top_languages: List[LanguageStat] = [
            LanguageStat(
                language=lang,
                bytes_count=count * 50000,
                percentage=round((count / total_lang_instances) * 100, 1),
                repo_count=count,
            )
            for lang, count in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]

        # Determine primary role
        primary_lang = top_languages[0].language.lower() if top_languages else "python"
        if primary_lang in ["javascript", "typescript", "html", "css", "vue", "svelte"]:
            primary_role = PrimaryRole.FRONTEND
        elif primary_lang in ["go", "rust", "c", "c++", "zig"]:
            primary_role = PrimaryRole.SYSTEMS
        elif primary_lang in ["dart", "swift", "kotlin"]:
            primary_role = PrimaryRole.MOBILE
        elif any(kw in (user_data.get("bio") or "").lower() for kw in ["ai", "ml", "data", "deep learning"]):
            primary_role = PrimaryRole.AIML
        else:
            primary_role = PrimaryRole.BACKEND

        # Determine tier
        repo_count = user_data.get("public_repos", 0)
        followers = user_data.get("followers", 0)
        if repo_count > 40 or total_stars > 200 or followers > 150:
            tier = ExperienceTier.SENIOR
        elif repo_count > 15 or total_stars > 20:
            tier = ExperienceTier.INTERMEDIATE
        else:
            tier = ExperienceTier.BEGINNER

        return DeveloperProfile(
            username=user_data.get("login", ""),
            name=user_data.get("name") or user_data.get("login"),
            avatar_url=user_data.get("avatar_url", ""),
            bio=user_data.get("bio") or "Passionate software developer on GitHub.",
            company=user_data.get("company"),
            location=user_data.get("location"),
            public_repos_count=repo_count,
            total_stars_received=total_stars,
            followers_count=followers,
            following_count=user_data.get("following", 0),
            primary_role=primary_role,
            experience_tier=tier,
            top_languages=top_languages,
            skill_tags=[l.language for l in top_languages] + [primary_role.value],
            domain_interests=["Open Source", "Software Engineering", primary_role.value],
            coding_rhythm=CodingRhythm.BALANCED,
            night_owl_score=0.55,
            weekend_activity_ratio=0.28,
            featured_repos=featured_repos,
            open_to_collaborate=True,
            ai_summary=f"Developer with strong focus on {primary_lang.title()} and {primary_role.value}.",
        )

    def _build_synthetic_profile(self, username: str) -> DeveloperProfile:
        """Create a placeholder developer profile when username is not found."""
        return DeveloperProfile(
            username=username,
            name=username.replace("-", " ").replace("_", " ").title(),
            avatar_url=f"https://api.dicebear.com/7.x/identicon/svg?seed={username}",
            bio=f"Open source developer and software engineer @{username}.",
            public_repos_count=10,
            total_stars_received=12,
            followers_count=8,
            following_count=12,
            primary_role=PrimaryRole.FULLSTACK,
            experience_tier=ExperienceTier.INTERMEDIATE,
            top_languages=[
                LanguageStat(language="Python", bytes_count=120000, percentage=60.0, repo_count=6),
                LanguageStat(language="TypeScript", bytes_count=80000, percentage=40.0, repo_count=4),
            ],
            skill_tags=["Python", "TypeScript", "FastAPI", "React", "Docker"],
            domain_interests=["Fullstack Apps", "APIs", "Open Source"],
            coding_rhythm=CodingRhythm.BALANCED,
            night_owl_score=0.5,
            weekend_activity_ratio=0.25,
            featured_repos=[
                RepositorySummary(
                    name=f"{username}-project",
                    description="Personal software development repository",
                    html_url=f"https://github.com/{username}/{username}-project",
                    language="Python",
                    stargazers_count=5,
                    forks_count=1,
                    topics=["developer", "open-source"],
                )
            ],
            open_to_collaborate=True,
            ai_summary="Adaptive full-stack engineer looking for collaboration and open-source opportunities.",
        )

    async def list_community_developers(self) -> List[DeveloperProfile]:
        """Return all curated community developers available for matchmaking."""
        profiles = []
        for username in SEED_DEVELOPERS:
            p = await self.get_developer_profile(username)
            profiles.append(p)
        return profiles


github_client = GitHubClient()
