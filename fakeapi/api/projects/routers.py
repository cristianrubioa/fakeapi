from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status

from fakeapi.api.projects import services
from fakeapi.api.projects.models import ProjectCreateModel
from fakeapi.api.projects.models import ProjectResponseModel
from fakeapi.api.projects.models import ProjectUpdateModel
from fakeapi.api.tasks import services as task_services
from fakeapi.api.workspaces.dependencies import get_workspace
from fakeapi.common.decorators import filter
from fakeapi.common.decorators import paginate
from fakeapi.common.decorators import sort
from fakeapi.common.pagination import PaginationPreset
from fakeapi.storage.base import WorkspaceData

router = APIRouter()


@router.post("/", response_model=ProjectResponseModel, status_code=status.HTTP_201_CREATED)
async def create_project_route(
    new_project: ProjectCreateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> ProjectResponseModel:
    return services.create_project(new_project, workspace)


@router.get("/", response_model=dict[str, Any])
@paginate(PaginationPreset.STANDARD)
@filter(filtering_fields={"id", "name", "status", "created_at"})
@sort(ordering_fields={"id", "name", "status", "created_at"})
async def get_projects(
    request: Request,
    workspace: WorkspaceData = Depends(get_workspace),
) -> dict[str, Any]:
    return services.get_projects_list(workspace)


@router.get("/{project_id}", response_model=ProjectResponseModel)
async def get_project_route(
    project_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> ProjectResponseModel:
    return services.get_project_by_id(project_id, workspace)


@router.patch("/{project_id}", response_model=ProjectResponseModel)
async def update_project_partial_route(
    project_id: int,
    project_updates: ProjectUpdateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> ProjectResponseModel:
    return services.update_project_partial(project_id, project_updates, workspace)


@router.put("/{project_id}", response_model=ProjectResponseModel)
async def update_project_route(
    project_id: int,
    new_project_data: ProjectUpdateModel,
    workspace: WorkspaceData = Depends(get_workspace),
) -> ProjectResponseModel:
    return services.update_project(project_id, new_project_data, workspace)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> None:
    services.delete_project_by_id(project_id, workspace)


@router.get("/{project_id}/tasks", response_model=dict[str, Any])
@paginate(PaginationPreset.STANDARD)
@filter(filtering_fields={"status", "user_id", "created_at"})
@sort(ordering_fields={"id", "title", "status", "created_at"})
async def get_project_tasks(
    request: Request,
    project_id: int,
    workspace: WorkspaceData = Depends(get_workspace),
) -> dict[str, Any]:
    services.get_project_by_id(project_id, workspace)
    all_tasks = task_services.get_tasks_list(workspace)
    return [t for t in all_tasks if t.project_id == project_id]
