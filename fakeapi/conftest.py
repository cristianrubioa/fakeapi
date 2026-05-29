import pytest
from starlette.testclient import TestClient

from fakeapi.main import app
from fakeapi.storage import storage


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module", autouse=True)
def clean_storage():
    storage.clear()


@pytest.fixture(scope="module")
def workspace_id(client):
    response = client.post("/api/workspaces/")
    return response.json()["id"]
