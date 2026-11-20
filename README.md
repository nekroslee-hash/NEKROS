# NEKROS

Modular personal AI assistant foundation.

## Included
- FastAPI backend and health endpoint
- SQLite persistent memory with local keyword retrieval
- Task creation and explicit approval workflow
- Automatic OpenRouter chat routing restricted to model IDs ending in `:free`
- Lightweight task hints for coding and reasoning model selection
- AI and media capability status endpoints
- Persian dark/red dashboard
- Initial automated tests

## Free-only AI setup
1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`.
5. Set a long random `NEKROS_API_TOKEN`.
6. Obtain an OpenRouter API key if available to your account and set `NEKROS_OPENROUTER_API_KEY`.
7. Add one or more currently available free model IDs to `NEKROS_FREE_MODELS`, separated by commas. Every model ID must end in `:free`. Paid model IDs are rejected by the router.
8. Run: `uvicorn nekros.main:app --reload`
9. Open `http://127.0.0.1:8000`.

The provider may still enforce free-tier rate limits or temporary availability. NEKROS does not silently switch to paid models. API keys belong only in the server-side `.env` file and must never be committed.

## Media generation status
The dashboard and API expose capability status for music, video, image, and voice. Actual generation adapters are not connected yet. They will only be enabled for official APIs with a genuinely free tier or local execution. A normal website account or browser session is not treated as an API, and subscription/download limits are not bypassed.

## API
- `/api/health` — public service health
- `/api/ai/status` — authenticated AI provider status
- `/api/media/capabilities` — authenticated media integration status
- `/docs` — interactive API documentation

This is a development foundation, not a finished always-on assistant. Do not expose it publicly without HTTPS, strong authentication, rate limiting, and deployment hardening. Voice, Android integration, local models, official media adapters, and background agent scheduling remain future milestones.
