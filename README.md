# DevOn – AI-Powered Developer Matchmaker

DevOn analyzes your GitHub activity, coding patterns, and collaboration history to find the most compatible developers for pair programming, open‑source contributions, and project co‑creation.

> **Status**: 🚧 Early development – MVP in progress. Contributions and ideas are welcome!

---

## 🎯 Why DevOn?

Finding a good coding partner is hard. Existing platforms rely on self‑reported skills or superficial social networks. DevOn uses **real data** from GitHub and **AI embeddings** to match developers based on:

- **Complementary skills** (e.g., you’re strong in frontend, they excel at backend)
- **Coding schedule compatibility** (night owls vs. morning larks)
- **Project interests** (languages, frameworks, starred repos)
- **Contribution quality** (issue resolution, PR reviews, documentation)

---

## ✨ Features (Planned & In Progress)

| Feature | Description | Status |
|---------|-------------|--------|
| GitHub OAuth Login | Secure authentication via GitHub | 🟡 Planned |
| Profile Analyzer | Extracts public repo data, languages, commit patterns | 🟢 In design |
| Embedding Generator | Converts profile into a vector using Gemini/OpenAI | 🟡 Planned |
| Smart Matchmaking | Finds compatible developers via vector similarity | 🟡 Planned |
| Collaboration Suggestions | Recommends specific issues or projects to tackle together | 🔴 Not started |
| AI Chat Assistant | Answers questions about matches and onboarding | 🔴 Not started |
| GitHub MCP Integration | Lets the AI create issues and PRs automatically | 🔴 Not started |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12+ (FastAPI) – *or Node.js (Express) – to be decided*
- **AI & Embeddings**: Google Gemini API (`text-embedding-004`) / OpenAI (`text-embedding-ada-002`)
- **Vector Database**: Pinecone (cloud) or `pgvector` (self‑hosted)
- **Relational DB**: PostgreSQL (for user profiles, match history)
- **API Client**: `httpx` / `PyGithub`
- **Frontend** (future): React + TailwindCSS
- **Version Control**: Git + GitHub Flow

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- A GitHub account
- (Optional) API keys for Gemini or OpenAI

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/DevOn.git
cd DevOn
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:

```env
GITHUB_CLIENT_ID=your_github_oauth_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_client_secret
GEMINI_API_KEY=your_gemini_api_key   # optional
OPENAI_API_KEY=your_openai_api_key   # optional
DATABASE_URL=postgresql://user:pass@localhost/devon
```

5. **Run the development server**

```bash
uvicorn backend.main:app --reload
```

---

## 📂 Project Structure

```
DevOn/
├── .github/                # Issue / PR templates, workflows
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── backend/
│   ├── api/                # FastAPI routes
│   ├── core/               # Config, security, database
│   ├── models/             # SQLAlchemy / Pydantic models
│   ├── services/           # GitHub client, embedding, matching
│   └── main.py
├── frontend/               # (future) React app
├── docs/                   # Detailed documentation
├── tests/                  # Unit and integration tests
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
└── README.md               # You are here
```

---

## 🤝 How to Contribute

We follow GitHub Flow – all changes happen via Pull Requests.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-amazing-idea
```

3. Commit your changes.
4. Push to your fork:

```bash
git push origin feature/your-amazing-idea
```

5. Open a Pull Request against the main branch.

---

## 📄 License
Distributed under the MIT License. See the LICENSE file for more information.

---

## 🙏 Acknowledgements
- GitHub REST API
- GitHub GraphQL API
- Open Source Guides
- Gemini API
- Python GitHub library (PyGithub)

---

## 📬 Contact & Community
- Open an issue
- Start a Discussion
- Join our future Discord

Built with ❤️ for the open‑source community.
