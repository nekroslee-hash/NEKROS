from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_token: str = "change-this-before-running"
    database_path: str = "nekros.db"
    model_config = SettingsConfigDict(env_prefix="NEKROS_", env_file=".env", extra="ignore")

settings = Settings()
