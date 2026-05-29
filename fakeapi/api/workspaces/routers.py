from fastapi import APIRouter
from fastapi import Request
from fastapi import status

from fakeapi.api.workspaces import services
from fakeapi.api.workspaces.models import WorkspaceCountResponseModel
from fakeapi.api.workspaces.models import WorkspaceResponseModel
from fakeapi.common.limiter import limiter
from fakeapi.settings import settings
from fakeapi.storage import storage

router = APIRouter()


def _to_response(ws) -> WorkspaceResponseModel:
    return WorkspaceResponseModel(
        id=ws.id,
        created_at=ws.created_at,
        expires_at=ws.expires_at,
        extend_count=ws.extend_count,
        plan=ws.plan,
    )


@router.post("/", response_model=WorkspaceResponseModel, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
@limiter.limit(settings.PLANS["free"]["rate_limit"])
async def create_workspace(request: Request) -> WorkspaceResponseModel:
    client_ip = request.headers.get("CF-Connecting-IP") or request.client.host
    ws = services.create_workspace(client_ip)
    return _to_response(ws)


@router.get("/{workspace_id}", response_model=WorkspaceResponseModel)
async def get_workspace(workspace_id: str) -> WorkspaceResponseModel:
    ws = services.get_workspace(workspace_id)
    return _to_response(ws)


@router.post("/{workspace_id}/extend", response_model=WorkspaceResponseModel)
async def extend_workspace(workspace_id: str) -> WorkspaceResponseModel:
    ws = services.extend_workspace(workspace_id)
    return _to_response(ws)


@router.post("/{workspace_id}/reset", response_model=WorkspaceResponseModel)
async def reset_workspace(workspace_id: str) -> WorkspaceResponseModel:
    ws = services.reset_workspace(workspace_id)
    return _to_response(ws)
