# NEKROS

Modular personal AI assistant foundation.

## Included
- FastAPI backend and health endpoint
- SQLite persistent memory
- Task creation
- Explicit approval workflow for sensitive actions
- Provider-neutral AI orchestrator (no paid provider is called by default)
- Black/red Persian dashboard
- Initial automated tests

## Run locally
1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set a long random `NEKROS_API_TOKEN`.
5. Run: `uvicorn nekros.main:app --reload`
6. Open `http://127.0.0.1:8000`.

API docs: `/docs`.

This is a development foundation, not a finished always-on assistant. Do not expose it publicly without HTTPS, strong authentication, rate limiting, and deployment hardening. Voice, Android integration, local models, provider adapters and background agent scheduling are later milestones.
