import os
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "Minecraft Server Control Panel"
    api_prefix: str = "/api/v1"
    secret_key: str = Field(default="change-me", env="SECRET_KEY")
    access_token_expire_minutes: int = 60
    db_url: str = Field(default="sqlite:///./data/app.db", env="DB_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    panel_port: int = Field(default=8443, env="PANEL_PORT")

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
