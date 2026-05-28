from unittest.mock import ANY

import httpx


def test_list_users(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/ws/{workspace_id}/users/")
    # Expected
    expected = {"count": 10, "next": None, "previous": None, "results": ANY}
    assert response.status_code == 200
    assert response.json() == expected


def test_filter_users_by_role(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/ws/{workspace_id}/users/?role=admin")
    # Expected
    data = response.json()
    assert response.status_code == 200
    assert all(item["role"] == "admin" for item in data["results"])


def test_get_user_by_id(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/ws/{workspace_id}/users/1")
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


def test_get_user_not_found(base_url, workspace_id):
    # Action
    response = httpx.get(f"{base_url}/ws/{workspace_id}/users/999999")
    # Expected
    expected = {"detail": "User not found."}
    assert response.status_code == 404
    assert response.json() == expected


def test_create_user(base_url, workspace_id):
    # Setup
    payload = {"name": "Smoke Tester", "email": "smoke@example.com", "role": "member"}
    # Action
    response = httpx.post(f"{base_url}/ws/{workspace_id}/users/", json=payload)
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "name": "Smoke Tester",
        "email": "smoke@example.com",
        "role": "member",
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_delete_user(base_url, workspace_id):
    # Setup
    created = httpx.post(
        f"{base_url}/ws/{workspace_id}/users/",
        json={"name": "Delete Target", "email": "delete@example.com", "role": "viewer"},
    ).json()
    user_id = created["id"]
    # Action
    response = httpx.delete(f"{base_url}/ws/{workspace_id}/users/{user_id}")
    # Expected
    assert response.status_code == 204
    assert response.content == b""
