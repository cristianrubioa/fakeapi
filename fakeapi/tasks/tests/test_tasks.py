import pytest
import pytest_asyncio
from fastapi import status
from httpx import ASGITransport
from httpx import AsyncClient

from fakeapi.main import app


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localtest") as client:
        yield client


@pytest.mark.asyncio
class TestTasksAPI:
    async def test_get_tasks_default(self, async_client):
        # Action
        response = await async_client.get("/tasks/")
        # Expected
        assert response.status_code == status.HTTP_200_OK

    async def test_get_single_task_success(self, async_client):
        # Action
        response = await async_client.get("/tasks/1")
        # Expected
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1

    async def test_get_single_task_not_found(self, async_client):
        # Action
        response = await async_client.get("/tasks/9999")
        # Expected
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Resource not found."

    async def test_create_task(self, async_client):
        # Setup
        new_task = {"title": "New Test Task", "description": "Testing task creation", "status": "pending"}
        # Action
        response = await async_client.post("/tasks/", json=new_task)
        # Expected
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["title"] == new_task["title"]

    async def test_update_task(self, async_client):
        # Setup
        edit_task = {"title": "Update Test Task"}
        # Action
        response = await async_client.patch("/tasks/3", json=edit_task)
        # Expected
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == edit_task["title"]

    async def test_delete_task(self, async_client):
        # Action
        response = await async_client.delete("/tasks/2")
        # Expected
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_get_tasks_with_sorting(self, async_client):
        # Action
        response = await async_client.get("/tasks/?sort_by=-id")
        # Expected
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["results"]
        ids = [task["id"] for task in data]
        assert ids == sorted(ids, reverse=True)

    async def test_get_tasks_with_filtering(self, async_client):
        # Action
        response = await async_client.get("/tasks/?status=pending")
        # Expected
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["results"]
        for task in data:
            assert task["status"] == "pending"

    async def test_get_tasks_with_pagination(self, async_client):
        # Action
        response = await async_client.get("/tasks/?page=1&page_size=5")
        # Expected
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert "results" in body
        assert body["count"] >= len(body["results"])
        assert body["next"] in [None, 2]
        assert body["previous"] is None
