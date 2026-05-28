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


@pytest_asyncio.fixture
async def workspace_id(async_client):
    response = await async_client.post("/workspaces/")
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


# ─── Workspace lifecycle ──────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestWorkspaceCreation:
    async def test_create_workspace_happy_path(self, async_client):
        response = await async_client.post("/workspaces/")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert data["plan"] == "free"
        assert data["extend_count"] == 0
        assert "expires_at" in data

    async def test_get_workspace(self, async_client, workspace_id):
        response = await async_client.get(f"/workspaces/{workspace_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == workspace_id

    async def test_get_unknown_workspace(self, async_client):
        response = await async_client.get("/workspaces/00000000-0000-0000-0000-000000000000")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestWorkspaceExtensionAndReset:
    async def test_extend_workspace(self, async_client, workspace_id):
        response = await async_client.post(f"/workspaces/{workspace_id}/extend")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["extend_count"] == 1

    async def test_extend_workspace_limit(self, async_client, workspace_id):
        for _ in range(3):
            await async_client.post(f"/workspaces/{workspace_id}/extend")
        response = await async_client.post(f"/workspaces/{workspace_id}/extend")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Maximum extensions reached" in response.json()["detail"]

    async def test_reset_workspace(self, async_client, workspace_id):
        await async_client.delete(f"/ws/{workspace_id}/tasks/1")
        response = await async_client.post(f"/workspaces/{workspace_id}/reset")
        assert response.status_code == status.HTTP_200_OK
        tasks_response = await async_client.get(f"/ws/{workspace_id}/tasks/1")
        assert tasks_response.status_code == status.HTTP_200_OK


# ─── Tasks ────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestTasksAPI:
    async def test_get_tasks_default(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/tasks/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.json()

    async def test_get_single_task_success(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/tasks/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1

    async def test_get_single_task_not_found(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/tasks/9999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Resource not found."

    async def test_create_task(self, async_client, workspace_id):
        new_task = {
            "title": "New Test Task",
            "description": "Testing task creation",
            "status": "pending",
        }
        response = await async_client.post(f"/ws/{workspace_id}/tasks/", json=new_task)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["title"] == new_task["title"]

    async def test_update_task(self, async_client, workspace_id):
        edit_task = {"title": "Update Test Task"}
        response = await async_client.patch(f"/ws/{workspace_id}/tasks/3", json=edit_task)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == edit_task["title"]

    async def test_delete_task(self, async_client, workspace_id):
        response = await async_client.delete(f"/ws/{workspace_id}/tasks/2")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_get_tasks_with_sorting(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/tasks/?sort_by=-id")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["results"]
        ids = [t["id"] for t in data]
        assert ids == sorted(ids, reverse=True)

    async def test_get_tasks_with_filtering(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/tasks/?status=pending")
        assert response.status_code == status.HTTP_200_OK
        for task in response.json()["results"]:
            assert task["status"] == "pending"

    async def test_get_tasks_with_pagination(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/tasks/?page=1&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert "results" in body
        assert body["count"] >= len(body["results"])
        assert body["next"] in [None, 2]
        assert body["previous"] is None

    async def test_task_fk_invalid_user_id(self, async_client, workspace_id):
        task = {
            "title": "FK Test Task",
            "description": "Testing FK validation",
            "user_id": 9999,
        }
        response = await async_client.post(f"/ws/{workspace_id}/tasks/", json=task)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "user_id not found" in response.json()["detail"]

    async def test_task_fk_invalid_project_id(self, async_client, workspace_id):
        task = {
            "title": "FK Test Task",
            "description": "Testing FK validation",
            "project_id": 9999,
        }
        response = await async_client.post(f"/ws/{workspace_id}/tasks/", json=task)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "project_id not found" in response.json()["detail"]

    async def test_filter_by_user_id(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/tasks/?user_id=1")
        assert response.status_code == status.HTTP_200_OK
        for task in response.json()["results"]:
            assert task["user_id"] == 1


# ─── Users ────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestUsersAPI:
    async def test_list_users(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 10

    async def test_get_user(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/users/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1

    async def test_get_user_not_found(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/users/9999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_create_user(self, async_client, workspace_id):
        new_user = {
            "name": "Test User",
            "email": "testuser@example.com",
            "role": "member",
        }
        response = await async_client.post(f"/ws/{workspace_id}/users/", json=new_user)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == new_user["email"]

    async def test_create_user_duplicate_email(self, async_client, workspace_id):
        user = {"name": "Duplicate", "email": "dup@example.com"}
        await async_client.post(f"/ws/{workspace_id}/users/", json=user)
        response = await async_client.post(f"/ws/{workspace_id}/users/", json=user)
        assert response.status_code == status.HTTP_409_CONFLICT

    async def test_patch_user(self, async_client, workspace_id):
        response = await async_client.patch(f"/ws/{workspace_id}/users/1", json={"name": "Updated Name"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated Name"

    async def test_delete_user(self, async_client, workspace_id):
        response = await async_client.delete(f"/ws/{workspace_id}/users/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_filter_users_by_role(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/users/?role=admin")
        assert response.status_code == status.HTTP_200_OK
        for user in response.json()["results"]:
            assert user["role"] == "admin"

    async def test_get_user_tasks(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/users/1/tasks")
        assert response.status_code == status.HTTP_200_OK
        for task in response.json()["results"]:
            assert task["user_id"] == 1


# ─── Projects ─────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestProjectsAPI:
    async def test_list_projects(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/projects/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 10

    async def test_get_project(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/projects/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == 1

    async def test_get_project_not_found(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/projects/9999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_create_project(self, async_client, workspace_id):
        new_project = {
            "name": "Test Project",
            "description": "A test project description.",
            "status": "active",
        }
        response = await async_client.post(f"/ws/{workspace_id}/projects/", json=new_project)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == new_project["name"]

    async def test_patch_project(self, async_client, workspace_id):
        response = await async_client.patch(f"/ws/{workspace_id}/projects/1", json={"status": "completed"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "completed"

    async def test_delete_project(self, async_client, workspace_id):
        response = await async_client.delete(f"/ws/{workspace_id}/projects/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_filter_projects_by_status(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/projects/?status=active")
        assert response.status_code == status.HTTP_200_OK
        for project in response.json()["results"]:
            assert project["status"] == "active"

    async def test_get_project_tasks(self, async_client, workspace_id):
        response = await async_client.get(f"/ws/{workspace_id}/projects/1/tasks")
        assert response.status_code == status.HTTP_200_OK
        for task in response.json()["results"]:
            assert task["project_id"] == 1


# ─── Workspace isolation ──────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestWorkspaceIsolation:
    async def test_two_workspaces_do_not_share_data(self, async_client):
        r1 = await async_client.post("/workspaces/")
        r2 = await async_client.post("/workspaces/")
        ws1 = r1.json()["id"]
        ws2 = r2.json()["id"]

        await async_client.delete(f"/ws/{ws1}/tasks/1")

        r_ws1 = await async_client.get(f"/ws/{ws1}/tasks/1")
        r_ws2 = await async_client.get(f"/ws/{ws2}/tasks/1")

        assert r_ws1.status_code == status.HTTP_404_NOT_FOUND
        assert r_ws2.status_code == status.HTTP_200_OK


# ─── Record limits ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestRecordLimits:
    async def test_task_record_limit(self, async_client, workspace_id):
        task = {"title": "Limit Test Task", "description": "Testing limit enforcement"}
        for i in range(70):
            await async_client.post(f"/ws/{workspace_id}/tasks/", json=task)
        response = await async_client.post(f"/ws/{workspace_id}/tasks/", json=task)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Resource limit reached" in response.json()["detail"]
