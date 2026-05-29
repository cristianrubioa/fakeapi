from unittest.mock import ANY


def test_list_tasks(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/api/workspaces/{workspace_id}/tasks/")
    # Expected
    expected = {
        "count": 30,
        "next": None,
        "previous": None,
        "results": ANY,
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_get_task_by_id(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/api/workspaces/{workspace_id}/tasks/1")
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


def test_get_task_not_found(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/api/workspaces/{workspace_id}/tasks/999999")
    # Expected
    expected = {"detail": "Resource not found."}
    assert response.status_code == 404
    assert response.json() == expected


def test_create_task(client, workspace_id):
    # Setup
    payload = {
        "title": "New Task Title",
        "description": "A new task description",
        "status": "pending",
        "user_id": None,
        "project_id": None,
    }
    # Action
    response = client.post(f"/api/workspaces/{workspace_id}/tasks/", json=payload)
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "title": "New Task Title",
        "description": "A new task description",
        "status": "pending",
        "user_id": None,
        "project_id": None,
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_patch_task(client, workspace_id):
    # Setup
    created = client.post(
        f"/api/workspaces/{workspace_id}/tasks/",
        json={"title": "Patch Target Task", "description": "Original description", "status": "pending"},
    ).json()
    task_id = created["id"]
    payload = {"title": "Patched Task Title", "status": "in_progress"}
    # Action
    response = client.patch(f"/api/workspaces/{workspace_id}/tasks/{task_id}", json=payload)
    # Expected
    expected = {
        "id": task_id,
        "created_at": ANY,
        "title": "Patched Task Title",
        "description": "Original description",
        "status": "in_progress",
        "user_id": None,
        "project_id": None,
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_delete_task(client, workspace_id):
    # Setup
    created = client.post(
        f"/api/workspaces/{workspace_id}/tasks/",
        json={"title": "Delete Target Task", "description": "To be deleted", "status": "pending"},
    ).json()
    task_id = created["id"]
    # Action
    response = client.delete(f"/api/workspaces/{workspace_id}/tasks/{task_id}")
    # Expected
    assert response.status_code == 204
    assert response.content == b""
