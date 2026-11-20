from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_token: str = "change-this-before-running"
    database_path: str = "nekros.db"
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    free_models: str = ""
    media_providers: str = ""
    model_config = SettingsConfigDict(env_prefix="NEKROS_", env_file=".env", extra="ignore")


settings = Settings()
