# DevOn Architecture Specification

DevOn is an **AI-powered developer matchmaker** that analyzes GitHub activities, commit patterns, language distributions, and domain interests to connect compatible coding partners for pair programming, open-source co-creation, and mentorship.

---

## 1. High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│              DevOn Frontend (Web Dashboard)             │
│   - Live GitHub Analyzer  - Interactive Match Simulator  │
│   - Side-by-Side Compare  - AI Collaboration Pitch Gen   │
└────────────────────────────┬─────────────────────────────┘
                             │ REST / JSON (HTTP)
                             ▼
┌──────────────────────────────────────────────────────────┐
│                   FastAPI Backend Core                   │
│   - CORS Middleware       - OAuth 2.0 Auth Flow          │
│   - Pydantic Settings     - Static Asset Serving         │
└────────────────────────────┬─────────────────────────────┘
                             │
     ┌───────────────────────┼───────────────────────┐
     ▼                       ▼                       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ GitHubClient │     │ Profile      │     │ Embedding    │
│ & Cache      │     │ Analyzer     │     │ Engine       │
│ - PyGithub   │     │ - Roles      │     │ - 128D Dense │
│ - REST API   │     │ - Rhythms    │     │   Vector     │
│ - Seed Store │     │ - Night Owl  │     │ - Gemini API │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                            ▼
               ┌───────────────────────────┐
               │     MatchmakerEngine      │
               │ - Multi-factor Scoring    │
               │ - Complementarity Matrix  │
               │ - Timezone Overlap        │
               │ - Experience Tier Pairing │
               └────────────┬──────────────┘
                            │
                            ▼
               ┌───────────────────────────┐
               │   CollaborationService    │
               │ & AI Pair Assistant       │
               │ - Project Concept Gen     │
               │ - Outreach Pitch Gen      │
               └───────────────────────────┘
```

---

## 2. Core Modules

### 2.1 Backend Structure
- `backend/core/`:
  - `config.py`: Environment configuration via Pydantic `BaseSettings`.
  - `security.py`: Secure tokens, hashing, and signature validation.
- `backend/models/`:
  - `developer.py`: Data models for GitHub stats, language breakdowns, and schedule rhythms.
  - `matching.py`: Models for matchmaking filters, compatibility breakdowns, and side-by-side comparison.
  - `collaboration.py`: Models for joint project ideas, outreach pitches, and conversational AI payloads.
- `backend/services/`:
  - `github_client.py`: High-throughput async client for GitHub REST API with caching and fallback seed developers.
  - `analyzer.py`: Behavioral analysis module calculating domain classification (Frontend, Backend, DevOps, Systems, AI/ML, Mobile) and circadian rhythm metrics.
  - `embedding.py`: AI Semantic Profile Vectorizer generating normalized dense feature vectors with cosine similarity calculation.
  - `matchmaker.py`: Multi-factor compatibility scoring engine supporting complementary, similar, peer, and mentorship pairing.
  - `collaboration.py`: AI-driven joint project concept and pitch generator.
  - `ai_assistant.py`: Interactive AI assistant endpoint for match Q&A and outreach icebreakers.
- `backend/api/v1/`:
  - `health.py`: Health check and system uptime telemetry.
  - `auth.py`: GitHub OAuth 2.0 authentication flow and session cookies.
  - `profiles.py`: User profile lookup, community directory, and live analysis.
  - `matchmaker.py`: Top partner recommendations and side-by-side developer comparison.
  - `collaboration.py`: Project concept generator and pitch crafting.
  - `ai_assistant.py`: Interactive AI assistant chat endpoint.

---

## 3. Data Flow

1. **User Ingestion**: A developer inputs their GitHub username or authenticates via GitHub OAuth.
2. **Profile Synthesis**: The `GitHubClient` retrieves public repo statistics, commit frequencies, and language breakdowns, which `ProfileAnalyzer` normalizes.
3. **Semantic Vectorization**: The `EmbeddingEngine` projects the synthesized profile into a 128-dimensional dense vector space.
4. **Candidate Matching**: The `MatchmakerEngine` evaluates the user against community candidates across four weighted axes:
   - Skill Complementarity (40%)
   - Schedule & Timezone Overlap (25%)
   - Domain Interests & Vector Similarity (20%)
   - Experience Tier Balance (15%)
5. **Collaboration Pitch Generation**: The `CollaborationService` synthesizes customized project ideas and icebreakers ready for outreach.
