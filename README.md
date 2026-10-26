# DevOn ⚡ – AI-Powered Developer Matchmaker

> **Find your ideal pair programming partner, open-source co-creator, and tech mentor through real GitHub telemetry, circadian rhythm analytics, and AI vector embeddings.**

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-25%20Passed-emerald.svg)](https://github.com/SoroushSoleimani/DevOn)

---

## 💡 Why DevOn?

Finding a compatible coding partner is notoriously hard. Existing platforms rely on self-reported questionnaires, outdated resumes, or superficial social connections. 

**DevOn changes that by analyzing actual engineering output on GitHub:**
- **Complementary Tech Stacks**: Pairs backend specialists with frontend architects, AI engineers with systems engineers, creating full-stack teams.
- **Circadian Schedule Compatibility**: Synchronizes your work hours (e.g. night owls pairing with night owls, or matching overlapping timezones).
- **Engineering Rhythm & Velocity**: Analyzes commit frequency, repository complexity, and weekend vs. weekday dedication.
- **AI Vector Embeddings**: Uses dense semantic vector projections and cosine similarity to match domain passions (e.g., distributed systems, agentic AI, WebAssembly).

---

## ✨ Features

- **🚀 Live GitHub Profile Analyzer**: Input any GitHub username to automatically synthesize their language breakdown, experience tier, and coding rhythm.
- **🧠 Multidimensional Matchmaking Engine**: Computes granular compatibility scores across Skill Complementarity, Schedule Sync, Domain Overlap, and Experience Tier Synergy.
- **🔍 4 Matching Strategies**:
  - `Complementary`: Cross-disciplinary synergy (Backend + Frontend, AI/ML + DevOps).
  - `Similar`: Same-stack mastery (Python specialist + Python specialist).
  - `Peer Learning`: Similar experience tiers for parallel exploration.
  - `Mentorship`: Senior / Staff engineers paired with Junior / Mid-level learners.
- **📊 Side-by-Side Comparison Modal**: Inspect two developers side-by-side with metric progress bars, shared synergies, and timezone gap analysis.
- **📋 AI Collaboration Pitch Generator**: Automatically drafts high-converting outreach icebreakers and proposes concrete joint project concepts tailored to both developers' skillsets.
- **🤖 Built-in AI Pair Assistant**: Slide-out assistant drawer to answer questions about schedule overlap, tech stack synergies, and icebreakers.
- **🎨 Glassmorphic Cyber-Minimalist Web Dashboard**: Modern, dark-mode single-page application served directly by FastAPI.

---

## 🏛️ System Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    DevOn Frontend Dashboard                   │
│   - Live GitHub Search       - Multi-factor Filters           │
│   - Side-by-Side Compare     - Collaboration Pitch & AI Chat  │
└───────────────────────────────┬───────────────────────────────┘
                                │ JSON REST API
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                     FastAPI Application                       │
│   /api/v1/profiles   /api/v1/matches   /api/v1/collaboration  │
└───────┬───────────────────────┬───────────────────────┬───────┘
        ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ GitHubClient │        │ Profile      │        │ Embedding    │
│ & TTL Cache  │───────►│ Analyzer     │───────►│ Engine       │
│ Live/Seed    │        │ Roles/Rhythm │        │ 128D Dense   │
└──────────────┘        └──────────────┘        └───────┬──────┘
                                                        │
                                                        ▼
                                            ┌───────────────────────┐
                                            │   MatchmakerEngine    │
                                            │ Overall Score (0-100) │
                                            └───────────────────────┘
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.12 or higher
- Git

### 2. Clone Repository
```bash
git clone https://github.com/SoroushSoleimani/DevOn.git
cd DevOn
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate       # On Linux/macOS
# or:
venv\Scripts\activate          # On Windows PowerShell
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment (Optional)
Copy the example configuration:
```bash
cp .env.example .env
```
*(DevOn runs out-of-the-box with built-in seed profiles and zero-dependency dense vectorizer even without API keys!)*

### 6. Run Application
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Open your browser and navigate to:
- **Web Dashboard**: [http://localhost:8000/](http://localhost:8000/)
- **Interactive OpenAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Tests

DevOn includes an automated test suite covering all services, vectorizers, matchmakers, and REST endpoints:

```bash
python -m pytest tests/ -v
```

Output:
```
tests/test_analyzer.py::test_classify_role_distribution PASSED
tests/test_analyzer.py::test_compute_rhythm_night_owl PASSED
tests/test_api.py::test_health_check_endpoint PASSED
tests/test_api.py::test_find_matches_endpoint PASSED
tests/test_matchmaker.py::test_evaluate_pair_complementary_synergy PASSED
...
======================== 25 passed in 9.04s ========================
```

---

## 📡 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/health` | `GET` | Health status and uptime |
| `/api/v1/profiles/{username}` | `GET` | Synthesized developer profile |
| `/api/v1/profiles/community` | `GET` | Directory of community developers |
| `/api/v1/matches/find/{username}` | `GET` | Top ranked compatible partners |
| `/api/v1/matches/compare` | `GET` | Side-by-side comparison between 2 developers |
| `/api/v1/collaboration/ideas` | `GET` | Tailored pair programming project ideas |
| `/api/v1/collaboration/pitch` | `GET` | AI outreach icebreaker pitch |
| `/api/v1/ai/chat` | `POST` | Conversational match consultant |

---

## 📐 Matchmaking Formula

The compatibility score between two developers is calculated as:

$$S_{total} = 0.40 \cdot S_{skill} + 0.25 \cdot S_{sched} + 0.20 \cdot S_{domain} + 0.15 \cdot S_{exp}$$

See [docs/MATCHING_ALGORITHM.md](docs/MATCHING_ALGORITHM.md) for full mathematical formulation.

---

## 📁 Repository Structure

```
DevOn/
├── backend/
│   ├── api/
│   │   └── v1/                 # REST Routers (auth, profiles, matches, collab, ai)
│   ├── core/                   # Settings, security, tokens
│   ├── models/                 # Pydantic domain models
│   ├── services/               # GitHubClient, ProfileAnalyzer, EmbeddingEngine, MatchmakerEngine
│   └── main.py                 # FastAPI application
├── frontend/
│   ├── css/style.css           # Glassmorphic dark theme design system
│   ├── js/app.js               # Reactive client application logic
│   └── index.html              # Modern dashboard layout
├── docs/
│   ├── ARCHITECTURE.md         # Component diagrams and data flow
│   └── MATCHING_ALGORITHM.md   # Mathematical compatibility model
├── tests/                      # Pytest unit & integration test suite (25 tests)
├── .env.example                # Config template
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
└── requirements.txt            # Python dependencies
```

---

## 📄 License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.

Developed with ❤️ by **[Soroush Soleimani](https://github.com/SoroushSoleimani)**.
