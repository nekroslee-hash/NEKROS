import secrets
from fastapi import Header, HTTPException
from .config import settings

async def require_token(authorization: str | None = Header(default=None)):
    if settings.api_token == "change-this-before-running":
        raise HTTPException(503, "Configure NEKROS_API_TOKEN in .env")
    if authorization is None or not secrets.compare_digest(authorization, "Bearer " + settings.api_token):
        raise HTTPException(401, "Unauthorized")
