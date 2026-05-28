from fastapi import HTTPException
from fastapi import Path
from fastapi import status

from fakeapi.storage import storage
from fakeapi.storage.base import WorkspaceData


def get_workspace(workspace_id: str = Path(...)) -> WorkspaceData:
    from datetime import UTC
    from datetime import datetime

    ws = storage.get(workspace_id)
    if ws is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found.")
    if ws.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Workspace has expired.")
    return ws
