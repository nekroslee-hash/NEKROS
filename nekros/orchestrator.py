"""Automatic, free-tier-only AI routing for NEKROS."""
from __future__ import annotations

import httpx
from .config import settings


class ProviderNotConfigured(RuntimeError):
    pass


def choose_free_model(prompt: str, models: list[str]) -> str:
    """Choose a configured free model using lightweight task hints."""
    allowed = [model.strip() for model in models if model.strip().endswith(":free")]
    if not allowed:
        raise ProviderNotConfigured(
            "هیچ مدل رایگان مجازی تنظیم نشده است. شناسه مدل رایگان را در NEKROS_FREE_MODELS قرار دهید."
        )

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
    """Routes requests only to explicitly configured free OpenRouter models."""

    def __init__(self):
        self.base_url = settings.openrouter_base_url.rstrip("/")

    def status(self) -> dict:
        models = self._models()
        configured = bool(settings.openrouter_api_key and models)
        return {
            "mode": "automatic",
            "provider": "openrouter",
            "configured": configured,
            "free_only": True,
            "available_models": models,
            "message": (
                "مسیریاب آماده است."
                if configured
                else "برای فعال‌شدن پاسخ هوشمند، کلید OpenRouter و حداقل یک مدل با پسوند :free لازم است."
            ),
        }

    @staticmethod
    def _models() -> list[str]:
        # Paid model IDs are discarded before they reach routing or status output.
        return [
            item.strip()
            for item in settings.free_models.split(",")
            if item.strip().endswith(":free")
        ]

    async def respond(self, prompt: str) -> str:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        if not settings.openrouter_api_key:
            raise ProviderNotConfigured(
                "اتصال هوش مصنوعی هنوز تنظیم نشده است؛ NEKROS برای استفاده رایگان به کلید API و مدل رایگان نیاز دارد."
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
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("پاسخ دریافتی از ارائه‌دهنده معتبر نیست.") from exc


orchestrator = AIOrchestrator()
