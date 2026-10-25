# Contributing to DevOn

We are thrilled that you are interested in contributing to **DevOn**! Whether you are fixing a bug, adding new matchmaking criteria, improving the UI, or writing documentation, all contributions are welcome.

---

## 1. Development Workflow

We follow standard **GitHub Flow**:

1. **Fork the Repository**: Fork [DevOn on GitHub](https://github.com/SoroushSoleimani/DevOn).
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DevOn.git
   cd DevOn
   ```
3. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```
5. **Run tests**:
   ```bash
   python -m pytest tests/ -v
   ```
6. **Commit with Conventional Commits**:
   - `feat(scope): ...` for new features
   - `fix(scope): ...` for bug fixes
   - `docs(scope): ...` for documentation
   - `test(scope): ...` for tests
   - `chore(scope): ...` for maintenance
7. **Open a Pull Request**: Submit your PR with a clear summary of your changes.

---

## 2. Code Standards

- **Python**: Follow PEP 8 guidelines and type hints (`typing`, `Pydantic`).
- **Tests**: Every new endpoint or service should have unit tests under `tests/`.
- **Aesthetics**: When contributing frontend features, adhere to the modern dark mode and glassmorphism design tokens.
