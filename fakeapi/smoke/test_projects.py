from unittest.mock import ANY

import httpx


def test_list_projects(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/projects/")
    # Expected
    expected = {"count": 10, "next": None, "previous": None, "results": ANY}
    assert response.status_code == 200
    assert response.json() == expected


def test_filter_projects_by_status(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/projects/?status=active")
    # Expected
    data = response.json()
    assert response.status_code == 200
    assert all(item["status"] == "active" for item in data["results"])


def test_get_project_by_id(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/projects/1")
    # Expected
    expected = {
        "id": 1,
        "name": "Core Platform v2",
        "description": "Full rebuild of the core platform with microservices architecture and improved scalability.",
        "status": "active",
        "created_at": "2024-01-01T00:00:00Z",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_get_project_not_found(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/api/workspaces/{workspace_id}/projects/999999")
    # Expected
    expected = {"detail": "Project not found."}
    assert response.status_code == 404
    assert response.json() == expected


def test_create_project(base_url, workspace_id):
    # Setup
    payload = {"name": "Smoke Project", "description": "Created by smoke suite", "status": "active"}
    # Action
    response = httpx.post(f"{base_url}/api/workspaces/{workspace_id}/projects/", json=payload)
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "name": "Smoke Project",
        "description": "Created by smoke suite",
        "status": "active",
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_delete_project(base_url, workspace_id):
    # Setup
    created = httpx.post(
        f"{base_url}/api/workspaces/{workspace_id}/projects/",
        json={"name": "Delete Target", "description": "To be deleted", "status": "active"},
    ).json()
    project_id = created["id"]
    # Action
    response = httpx.delete(f"{base_url}/api/workspaces/{workspace_id}/projects/{project_id}")
    # Expected
    assert response.status_code == 204
    assert response.content == b""
