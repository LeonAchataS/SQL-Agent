from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    openai_api_key: str
    
    # LLM Config
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0
    
    # App Config
    app_name: str = "SQL Agent"
    debug: bool = False
    database_url: str | None = None
    properties_limit: int = 5

@lru_cache
def get_settings() -> Settings:
    return Settings()

