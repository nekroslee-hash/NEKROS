"""Automatic, free-tier-only AI routing for NEKROS."""
from __future__ import annotations

import httpx
from .config import settings

FREE_ROUTER = "openrouter/free"


class ProviderNotConfigured(RuntimeError):
    pass


def choose_free_model(prompt: str, models: list[str]) -> str:
    """Choose a configured free model, or OpenRouter's free-only router."""
    supplied = [model.strip() for model in models if model.strip()]
    allowed = [model for model in supplied if model.endswith(":free") or model == FREE_ROUTER]
    if supplied and not allowed:
        raise ProviderNotConfigured(
            "هیچ مدل رایگان مجازی تنظیم نشده است. فقط مدل‌های دارای پسوند :free یا openrouter/free مجازند."
        )
    if not allowed:
        return FREE_ROUTER

    text = prompt.casefold()
    code_hints = ("python", "javascript", "html", "css", "کد", "برنامه‌نویسی", "خطا", "debug")
    reasoning_hints = ("تحلیل", "مقایسه", "استدلال", "چرا", "طراحی", "معماری", "برنامه‌ریزی")
    preferred = None
    if any(word in text for word in code_hints):
        preferred = next((m for m in allowed if any(x in m.casefold() for x in ("coder", "code", "qwen"))), None)
    elif any(word in text for word in reasoning_hints):
        preferred = next((m for m in allowed if any(x in m.casefold() for x in ("reason", "deepseek", "r1"))), None)
    return preferred or allowed[0]


class AIOrchestrator:
    """Routes requests only to explicitly free models or OpenRouter's free router."""

    def __init__(self):
        self.base_url = settings.openrouter_base_url.rstrip("/")

    @staticmethod
    def _models() -> list[str]:
        configured = [
            item.strip()
            for item in settings.free_models.split(",")
            if item.strip().endswith(":free")
        ]
        return configured or [FREE_ROUTER]

    def status(self) -> dict:
        models = self._models()
        configured = bool(settings.openrouter_api_key)
        return {
            "mode": "automatic",
            "provider": "openrouter",
            "configured": configured,
            "free_only": True,
            "available_models": models,
            "message": (
                "اتصال آماده است؛ مسیریاب OpenRouter فقط از مدل‌های رایگان استفاده می‌کند."
                if configured
                else "برای فعال‌شدن پاسخ هوشمند، کلید API رایگان OpenRouter را در تنظیمات سرور قرار دهید."
            ),
        }

    async def respond(self, prompt: str) -> str:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        if not settings.openrouter_api_key:
            raise ProviderNotConfigured(
                "اتصال هوش مصنوعی هنوز تنظیم نشده است؛ کلید API سرور OpenRouter لازم است."
            )
        model = choose_free_model(prompt, self._models())
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "X-Title": "NEKROS",
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1200,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise TypeError("Empty or non-text response")
            return content
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("پاسخ دریافتی از ارائه‌دهنده معتبر نیست.") from exc


orchestrator = AIOrchestrator()
