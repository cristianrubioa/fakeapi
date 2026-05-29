from unittest.mock import ANY

import httpx


def test_list_tasks(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/tasks/")
    # Expected
    expected = {"count": 30, "next": None, "previous": None, "results": ANY}
    assert response.status_code == 200
    assert response.json() == expected


def test_filter_tasks_by_status(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/tasks/?status=pending")
    # Expected
    data = response.json()
    assert response.status_code == 200
    assert all(item["status"] == "pending" for item in data["results"])


def test_pagination_moves_window(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/tasks/?page_size=5&page=2")
    # Expected
    data = response.json()
    assert response.status_code == 200
    assert len(data["results"]) == 5 and data["previous"] is not None


def test_get_task_by_id(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/tasks/1")
    # Expected
    expected = {
        "id": 1,
        "title": "AI-Powered CRM System",
        "description": "This project aims to modernize the customer relationship management system by integrating AI-powered analytics.",
        "status": "pending",
        "user_id": 1,
        "project_id": 1,
        "created_at": "2024-01-11T00:00:00Z",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_get_task_not_found(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/tasks/999999")
    # Expected
    expected = {"detail": "Resource not found."}
    assert response.status_code == 404
    assert response.json() == expected


def test_create_task(base_url, workspace_id):
    # Setup
    payload = {"title": "Smoke Test Task", "description": "Created by smoke suite", "status": "pending"}
    # Action
    response = httpx.post(f"{base_url}/api/workspaces/{workspace_id}/tasks/", json=payload)
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "title": "Smoke Test Task",
        "description": "Created by smoke suite",
        "status": "pending",
        "user_id": None,
        "project_id": None,
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_patch_task(base_url, workspace_id):
    # Setup
    created = httpx.post(
        f"{base_url}/api/workspaces/{workspace_id}/tasks/",
        json={"title": "Patch Target", "description": "Original", "status": "pending"},
    ).json()
    task_id = created["id"]
    # Action
    response = httpx.patch(f"{base_url}/api/workspaces/{workspace_id}/tasks/{task_id}", json={"status": "in_progress"})
    # Expected
    expected = {
        "id": task_id,
        "created_at": ANY,
        "title": "Patch Target",
        "description": "Original",
        "status": "in_progress",
        "user_id": None,
        "project_id": None,
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_delete_task(base_url, workspace_id):
    # Setup
    created = httpx.post(
        f"{base_url}/api/workspaces/{workspace_id}/tasks/",
        json={"title": "Delete Target", "description": "To be deleted", "status": "pending"},
    ).json()
    task_id = created["id"]
    # Action
    response = httpx.delete(f"{base_url}/api/workspaces/{workspace_id}/tasks/{task_id}")
    # Expected
    assert response.status_code == 204
    assert response.content == b""
