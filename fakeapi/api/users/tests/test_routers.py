from unittest.mock import ANY


def test_list_users(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/ws/{workspace_id}/users/")
    # Expected
    expected = {
        "count": 10,
        "next": None,
        "previous": None,
        "results": ANY,
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_get_user_by_id(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/ws/{workspace_id}/users/1")
    # Expected
    expected = {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "role": "admin",
        "created_at": "2024-01-01T00:00:00Z",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_get_user_not_found(client, workspace_id):
    # Setup
    # Action
    response = client.get(f"/ws/{workspace_id}/users/999999")
    # Expected
    expected = {"detail": "User not found."}
    assert response.status_code == 404
    assert response.json() == expected


def test_create_user(client, workspace_id):
    # Setup
    payload = {
        "name": "New User",
        "email": "new.user@example.com",
        "role": "member",
    }
    # Action
    response = client.post(f"/ws/{workspace_id}/users/", json=payload)
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "name": "New User",
        "email": "new.user@example.com",
        "role": "member",
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_create_user_duplicate_email(client, workspace_id):
    # Setup
    payload = {
        "name": "Duplicate User",
        "email": "alice.johnson@example.com",
        "role": "member",
    }
    # Action
    response = client.post(f"/ws/{workspace_id}/users/", json=payload)
    # Expected
    expected = {"detail": "Email already exists in this workspace."}
    assert response.status_code == 409
    assert response.json() == expected


def test_patch_user(client, workspace_id):
    # Setup
    created = client.post(
        f"/ws/{workspace_id}/users/",
        json={"name": "Patch Target", "email": "patch.target@example.com", "role": "member"},
    ).json()
    user_id = created["id"]
    payload = {"name": "Patched Name", "role": "viewer"}
    # Action
    response = client.patch(f"/ws/{workspace_id}/users/{user_id}", json=payload)
    # Expected
    expected = {
        "id": user_id,
        "created_at": ANY,
        "name": "Patched Name",
        "email": "patch.target@example.com",
        "role": "viewer",
    }
    assert response.status_code == 200
    assert response.json() == expected


def test_delete_user(client, workspace_id):
    # Setup
    created = client.post(
        f"/ws/{workspace_id}/users/",
        json={"name": "Delete Target", "email": "delete.target@example.com", "role": "member"},
    ).json()
    user_id = created["id"]
    # Action
    response = client.delete(f"/ws/{workspace_id}/users/{user_id}")
    # Expected
    assert response.status_code == 204
    assert response.content == b""
