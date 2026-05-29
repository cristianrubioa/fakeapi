from unittest.mock import ANY


def test_get_workspace_count_empty(client):
    # Action
    response = client.get("/api/workspaces/count")
    # Expected
    expected = {"count": 0, "limit": 3}
    assert response.status_code == 200
    assert response.json() == expected


def test_get_workspace_count_with_workspace(client, workspace_id):
    # Action
    response = client.get("/api/workspaces/count")
    # Expected
    expected = {"count": 1, "limit": 3}
    assert response.status_code == 200
    assert response.json() == expected


def test_create_workspace(client):
    # Action
    response = client.post("/api/workspaces/")
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "expires_at": ANY,
        "extend_count": 0,
        "plan": "free",
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_get_workspace(client, workspace_id):
    # Action
    response = client.get(f"/api/workspaces/{workspace_id}")
    # Expected
    expected = {
        "id": workspace_id,
        "created_at": ANY,
        "expires_at": ANY,
        "extend_count": 0,
        "plan": "free",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_get_workspace_not_found(client):
    # Action
    response = client.get("/api/workspaces/nonexistent-workspace-id")
    # Expected
    expected = {"detail": "Workspace not found."}
    assert response.status_code == 404
    assert response.json() == expected


def test_extend_workspace(client, workspace_id):
    # Action
    response = client.post(f"/api/workspaces/{workspace_id}/extend")
    # Expected
    expected = {
        "id": workspace_id,
        "created_at": ANY,
        "expires_at": ANY,
        "extend_count": 1,
        "plan": "free",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_extend_workspace_max_extensions_reached(client):
    # Setup
    ws_id = client.post("/api/workspaces/").json()["id"]
    for _ in range(3):
        client.post(f"/api/workspaces/{ws_id}/extend")
    # Action
    response = client.post(f"/api/workspaces/{ws_id}/extend")
    # Expected
    expected = {"detail": "Maximum extensions reached."}
    assert response.status_code == 422
    assert response.json() == expected


def test_reset_workspace(client, workspace_id):
    # Action
    response = client.post(f"/api/workspaces/{workspace_id}/reset")
    # Expected
    expected = {
        "id": workspace_id,
        "created_at": ANY,
        "expires_at": ANY,
        "extend_count": 1,
        "plan": "free",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_root(client):
    # Action
    response = client.get("/")
    # Expected
    assert response.status_code == 200


def test_admin_stats(client):
    # Action
    response = client.get("/api/admin/stats")
    # Expected
    expected = {
        "active_workspaces": ANY,
        "uptime_seconds": ANY,
    }
    assert response.status_code == 200
    assert response.json() == expected
