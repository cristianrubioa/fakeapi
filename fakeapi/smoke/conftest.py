import os

import httpx
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ["SMOKE_BASE_URL"].rstrip("/")


@pytest.fixture(scope="session")
def workspace_id(base_url: str) -> str:
    response = httpx.post(f"{base_url}/workspaces/")
    assert response.status_code == 201
    return response.json()["id"]
