from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@db:5432/urlshortener"
    REDIS_URL: str = "redis://redis:6379/0"
    STREAM_NAME: str = "analytics_stream"
    GROUP_NAME: str = "analytics_group"

settings = Settings()