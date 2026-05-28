from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status

from fakeapi.common.decorators import filter
from fakeapi.common.decorators import paginate
from fakeapi.common.decorators import sort
from fakeapi.common.pagination import PaginationPreset
from fakeapi.storage.base import WorkspaceData
from fakeapi.tasks import services as task_services
from fakeapi.users import services
from fakeapi.users.models import UserCreateModel
from fakeapi.users.models import UserResponseModel
from fakeapi.users.models import UserUpdateModel
from fakeapi.workspaces.dependencies import get_workspace

router = APIRouter()


@router.post("/", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user_route(
    new_user: UserCreateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> UserResponseModel:
    return services.create_user(new_user, workspace)


@router.get("/", response_model=dict[str, Any])
@paginate(PaginationPreset.STANDARD)
@filter(filtering_fields={"id", "name", "email", "role", "created_at"})
@sort(ordering_fields={"id", "name", "email", "role", "created_at"})
async def get_users(
    request: Request,
    workspace: WorkspaceData = Depends(get_workspace),
) -> dict[str, Any]:
    return services.get_users_list(workspace)


@router.get("/{user_id}", response_model=UserResponseModel)
async def get_user_route(
    user_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> UserResponseModel:
    return services.get_user_by_id(user_id, workspace)


@router.patch("/{user_id}", response_model=UserResponseModel)
async def update_user_partial_route(
    user_id: int,
    user_updates: UserUpdateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> UserResponseModel:
    return services.update_user_partial(user_id, user_updates, workspace)


@router.put("/{user_id}", response_model=UserResponseModel)
async def update_user_route(
    user_id: int,
    new_user_data: UserUpdateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> UserResponseModel:
    return services.update_user(user_id, new_user_data, workspace)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> None:
    services.delete_user_by_id(user_id, workspace)


@router.get("/{user_id}/tasks", response_model=dict[str, Any])
@paginate(PaginationPreset.STANDARD)
@filter(filtering_fields={"status", "project_id", "created_at"})
@sort(ordering_fields={"id", "title", "status", "created_at"})
async def get_user_tasks(
    request: Request,
    user_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> dict[str, Any]:
    services.get_user_by_id(user_id, workspace)
    all_tasks = task_services.get_tasks_list(workspace)
    return [t for t in all_tasks if t.user_id == user_id]
