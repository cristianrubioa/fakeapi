import uuid
from datetime import UTC
from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException
from fastapi import status

from fakeapi.seed import get_seed_snapshot
from fakeapi.settings import settings
from fakeapi.storage import storage
from fakeapi.storage.base import WorkspaceData


def _plan(plan_name: str) -> dict:
    return settings.PLANS[plan_name]


def create_workspace(client_ip: str) -> WorkspaceData:
    plan = _plan("free")

    if storage.total_count() >= plan["max_workspaces_global"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server at capacity. Try again later.",
        )

    if storage.count_by_ip(client_ip) >= plan["max_workspaces_per_ip"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workspace limit per IP reached.",
        )

    now = datetime.now(UTC)
    snapshot = get_seed_snapshot()
    workspace = WorkspaceData(
        id=str(uuid.uuid4()),
        created_at=now,
        expires_at=now + timedelta(hours=plan["ttl_hours"]),
        created_by_ip=client_ip,
        tasks=snapshot["tasks"],
        users=snapshot["users"],
        projects=snapshot["projects"],
    )
    storage.create(workspace)
    return workspace


def get_workspace(workspace_id: str) -> WorkspaceData:
    ws = storage.get(workspace_id)
    if ws is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found.")
    if ws.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Workspace has expired.")
    return ws


def extend_workspace(workspace_id: str) -> WorkspaceData:
    ws = get_workspace(workspace_id)
    max_ext = _plan(ws.plan)["max_extensions"]
    if ws.extend_count >= max_ext:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Maximum extensions reached.",
        )
    ws.extend_count += 1
    ws.expires_at = ws.expires_at + timedelta(hours=24)
    return ws


def reset_workspace(workspace_id: str) -> WorkspaceData:
    ws = get_workspace(workspace_id)
    snapshot = get_seed_snapshot()
    storage.set_resource(workspace_id, "tasks", snapshot["tasks"])
    storage.set_resource(workspace_id, "users", snapshot["users"])
    storage.set_resource(workspace_id, "projects", snapshot["projects"])
    return ws


def cleanup_expired() -> int:
    now = datetime.now(UTC)
    expired = [ws.id for ws in storage.list_all() if ws.expires_at < now]
    for ws_id in expired:
        storage.delete(ws_id)
    return len(expired)
