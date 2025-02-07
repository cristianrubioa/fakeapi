from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE_LIMITS: dict[str, int] = {"min": 5, "max": 100}
    DESCRIPTION_LIMITS: dict[str, int] = {"min": 1, "max": 300}

    class Config:
        env_prefix = "FakeAPI_"
        env_file = ".env"
        extra = "forbid"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
