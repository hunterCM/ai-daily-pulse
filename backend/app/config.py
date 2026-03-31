from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "AI Daily Pulse"
    environment: str = "development"
    database_url: str = "sqlite:///./ai_daily_pulse.db"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    resend_api_key: str = ""
    from_email: str = "AI Daily Pulse <briefs@aidailypulse.com>"
    admin_email: str = "inayethg777@gmail.com"

    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "AI Daily Pulse News Aggregator v1.0"

    brief_hour: int = 7
    brief_minute: int = 0
    timezone: str = "Africa/Johannesburg"

    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
