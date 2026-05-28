from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Optional


@dataclass
class WorkspaceData:
    id: str
    created_at: datetime
    expires_at: datetime
    created_by_ip: str
    extend_count: int = 0
    plan: str = "free"
    owner_id: Optional[str] = None
    tasks: list[dict] = field(default_factory=list)
    users: list[dict] = field(default_factory=list)
    projects: list[dict] = field(default_factory=list)


class WorkspaceStorage(ABC):
    @abstractmethod
    def get(self, workspace_id: str) -> Optional[WorkspaceData]: ...

    @abstractmethod
    def create(self, workspace: WorkspaceData) -> None: ...

    @abstractmethod
    def delete(self, workspace_id: str) -> None: ...

    @abstractmethod
    def get_resource(self, workspace_id: str, resource: str) -> list[dict]: ...

    @abstractmethod
    def set_resource(self, workspace_id: str, resource: str, data: list[dict]) -> None: ...

    @abstractmethod
    def list_all(self) -> list[WorkspaceData]: ...

    @abstractmethod
    def count_by_ip(self, ip: str) -> int: ...

    @abstractmethod
    def total_count(self) -> int: ...

    @abstractmethod
    def clear(self) -> None: ...
