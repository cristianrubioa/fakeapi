from typing import Optional

from fakeapi.storage.base import WorkspaceData
from fakeapi.storage.base import WorkspaceStorage


class InMemoryStorage(WorkspaceStorage):
    def __init__(self):
        self._workspaces: dict[str, WorkspaceData] = {}

    def get(self, workspace_id: str) -> Optional[WorkspaceData]:
        return self._workspaces.get(workspace_id)

    def create(self, workspace: WorkspaceData) -> None:
        self._workspaces[workspace.id] = workspace

    def delete(self, workspace_id: str) -> None:
        self._workspaces.pop(workspace_id, None)

    def get_resource(self, workspace_id: str, resource: str) -> list[dict]:
        return getattr(self._workspaces[workspace_id], resource)

    def set_resource(self, workspace_id: str, resource: str, data: list[dict]) -> None:
        setattr(self._workspaces[workspace_id], resource, data)

    def list_all(self) -> list[WorkspaceData]:
        return list(self._workspaces.values())

    def count_by_ip(self, ip: str) -> int:
        return sum(1 for ws in self._workspaces.values() if ws.created_by_ip == ip)

    def total_count(self) -> int:
        return len(self._workspaces)

    def clear(self) -> None:
        self._workspaces.clear()
