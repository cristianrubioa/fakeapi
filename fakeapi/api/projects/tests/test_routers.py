from unittest.mock import ANY


def test_list_projects(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/api/workspaces/{workspace_id}/projects/")
    # Expected
    expected = {
        "count": 10,
        "next": None,
        "previous": None,
        "results": ANY,
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_get_project_by_id(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/api/workspaces/{workspace_id}/projects/1")
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


def test_get_project_not_found(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/api/workspaces/{workspace_id}/projects/999999")
    # Expected
    expected = {"detail": "Project not found."}
    assert response.status_code == 404
    assert response.json() == expected


def test_create_project(client, workspace_id):
    # Setup
    payload = {
        "name": "New Project",
        "description": "A new project description",
        "status": "active",
    }
    # Action
    response = client.post(f"/api/workspaces/{workspace_id}/projects/", json=payload)
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "name": "New Project",
        "description": "A new project description",
        "status": "active",
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_patch_project(client, workspace_id):
    # Setup
    created = client.post(
        f"/api/workspaces/{workspace_id}/projects/",
        json={"name": "Patch Target", "description": "Original description", "status": "active"},
    ).json()
    project_id = created["id"]
    payload = {"name": "Patched Name"}
    # Action
    response = client.patch(f"/api/workspaces/{workspace_id}/projects/{project_id}", json=payload)
    # Expected
    expected = {
        "id": project_id,
        "created_at": ANY,
        "name": "Patched Name",
        "description": "Original description",
        "status": "active",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_put_project(client, workspace_id):
    # Setup
    created = client.post(
        f"/api/workspaces/{workspace_id}/projects/",
        json={"name": "Put Target", "description": "Original description", "status": "active"},
    ).json()
    project_id = created["id"]
    payload = {
        "name": "Updated Name",
        "description": "Updated description",
        "status": "on_hold",
    }
    # Action
    response = client.put(f"/api/workspaces/{workspace_id}/projects/{project_id}", json=payload)
    # Expected
    expected = {
        "id": project_id,
        "created_at": ANY,
        "name": "Updated Name",
        "description": "Updated description",
        "status": "on_hold",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_delete_project(client, workspace_id):
    # Setup
    created = client.post(
        f"/api/workspaces/{workspace_id}/projects/",
        json={"name": "Delete Target", "description": "To be deleted", "status": "active"},
    ).json()
    project_id = created["id"]
    # Action
    response = client.delete(f"/api/workspaces/{workspace_id}/projects/{project_id}")
    # Expected
    assert response.status_code == 204
    assert response.content == b""
