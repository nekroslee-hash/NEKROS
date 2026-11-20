"""Media-provider capability registry.

This module deliberately reports unavailable integrations as unavailable.
It does not pretend that a website account or a browser session is an API.
"""
from .config import settings

MEDIA_TYPES = ("music", "video", "image", "voice")


def media_status() -> dict:
    configured = [name.strip() for name in settings.media_providers.split(",") if name.strip()]
    return {
        "budget": "free",
        "automatic": True,
        "media_types": {
            media_type: {
                "available": False,
                "provider": None,
                "status": "not_configured",
            }
            for media_type in MEDIA_TYPES
        },
        "configured_provider_names": configured,
        "note": (
            "اتصال تولید رسانه هنوز فعال نیست. فقط API رسمی با سهمیه رایگان یا اجرای محلی مجاز است؛ "
            "هیچ سرویس پولی یا محدودیت دانلود دور زده نمی‌شود."
        ),
    }
