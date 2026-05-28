from fakeapi.settings import settings
from fakeapi.storage.base import WorkspaceData
from fakeapi.storage.base import WorkspaceStorage
from fakeapi.storage.enums import StorageBackend


def get_storage() -> WorkspaceStorage:
    if settings.STORAGE_BACKEND == StorageBackend.MEMORY:
        from fakeapi.storage.memory import InMemoryStorage

        return InMemoryStorage()
    raise ValueError(f"Unknown storage backend: {settings.STORAGE_BACKEND}")


storage: WorkspaceStorage = get_storage()

__all__ = ["storage", "WorkspaceData", "WorkspaceStorage"]
