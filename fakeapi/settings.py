from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings

from fakeapi.storage.enums import StorageBackend


class Settings(BaseSettings):
    TITLE_LIMITS: dict[str, int] = {"min": 5, "max": 100}
    DESCRIPTION_LIMITS: dict[str, int] = {"min": 1, "max": 300}

    STORAGE_BACKEND: StorageBackend = StorageBackend.MEMORY

    PLANS: dict[str, dict[str, Any]] = {
        "free": {
            "max_records_per_resource": 100,
            "ttl_hours": 24,
            "max_extensions": 3,
            "rate_limit": "60/minute",
            "max_workspaces_per_ip": 3,
            "max_workspaces_global": 200,
        }
    }

    class Config:
        env_prefix = "FakeAPI_"
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
