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
from fakeapi.tasks import services
from fakeapi.tasks.models import TaskCreateModel
from fakeapi.tasks.models import TaskResponseModel
from fakeapi.tasks.models import TaskUpdateModel
from fakeapi.workspaces.dependencies import get_workspace

router = APIRouter()


@router.post("/", response_model=TaskResponseModel, status_code=status.HTTP_201_CREATED)
async def create_task_route(
    new_task: TaskCreateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> TaskResponseModel:
    return services.create_task(new_task, workspace)


@router.get("/", response_model=dict[str, Any])
@paginate(PaginationPreset.STANDARD)
@filter(
    filtering_fields={
        "id",
        "title",
        "description",
        "status",
        "created_at",
        "user_id",
        "project_id",
    }
)
@sort(ordering_fields={"id", "title", "description", "status", "created_at"})
async def get_tasks(
    request: Request,
    workspace: WorkspaceData = Depends(get_workspace),
) -> dict[str, Any]:
    return services.get_tasks_list(workspace)


@router.get("/{task_id}", response_model=TaskResponseModel)
async def get_task_route(
    task_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> TaskResponseModel:
    return services.get_task_by_id(task_id, workspace)


@router.patch("/{task_id}", response_model=TaskResponseModel)
async def update_task_partial_route(
    task_id: int,
    task_updates: TaskUpdateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> TaskResponseModel:
    return services.update_task_partial(task_id, task_updates, workspace)


@router.put("/{task_id}", response_model=TaskResponseModel)
async def update_task_route(
    task_id: int,
    new_task_data: TaskUpdateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> TaskResponseModel:
    return services.update_task(task_id, new_task_data, workspace)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> None:
    services.delete_task_by_id(task_id, workspace)
