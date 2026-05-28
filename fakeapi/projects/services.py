from datetime import UTC
from datetime import datetime

from fastapi import HTTPException
from fastapi import status

from fakeapi.projects.exceptions import ProjectNotFoundError
from fakeapi.projects.models import ProjectCreateModel
from fakeapi.projects.models import ProjectResponseModel
from fakeapi.projects.models import ProjectUpdateModel
from fakeapi.settings import settings
from fakeapi.storage import storage
from fakeapi.storage.base import WorkspaceData


def _projects(workspace: WorkspaceData) -> list[dict]:
    return storage.get_resource(workspace.id, "projects")


def get_projects_list(workspace: WorkspaceData) -> list[ProjectResponseModel]:
    return [ProjectResponseModel(**p) for p in _projects(workspace)]


def get_project_by_id(project_id: int, workspace: WorkspaceData) -> ProjectResponseModel:
    project = next((p for p in _projects(workspace) if p["id"] == project_id), None)
    if project is None:
        raise ProjectNotFoundError()
    return ProjectResponseModel(**project)


def create_project(new_project: ProjectCreateModel, workspace: WorkspaceData) -> ProjectResponseModel:
    projects = _projects(workspace)
    limit = settings.PLANS[workspace.plan]["max_records_per_resource"]
    if len(projects) >= limit:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Resource limit reached for this workspace.",
        )

    new_id = max((p["id"] for p in projects), default=0) + 1
    project_data = {
        "id": new_id,
        "name": new_project.name,
        "description": new_project.description,
        "status": new_project.status,
        "created_at": datetime.now(UTC),
    }
    projects.append(project_data)
    return ProjectResponseModel(**project_data)


def update_project(
    project_id: int, new_project_data: ProjectUpdateModel, workspace: WorkspaceData
) -> ProjectResponseModel:
    projects = _projects(workspace)
    project_dict = next((p for p in projects if p["id"] == project_id), None)
    if project_dict is None:
        raise ProjectNotFoundError()
    project_dict.update(
        {
            "name": new_project_data.name,
            "description": new_project_data.description,
            "status": new_project_data.status,
        }
    )
    return ProjectResponseModel(**project_dict)


def update_project_partial(
    project_id: int, project_updates: ProjectUpdateModel, workspace: WorkspaceData
) -> ProjectResponseModel:
    projects = _projects(workspace)
    project_dict = next((p for p in projects if p["id"] == project_id), None)
    if project_dict is None:
        raise ProjectNotFoundError()
    project_dict.update(project_updates.model_dump(exclude_unset=True))
    return ProjectResponseModel(**project_dict)


def delete_project_by_id(project_id: int, workspace: WorkspaceData) -> None:
    projects = _projects(workspace)
    idx = next((i for i, p in enumerate(projects) if p["id"] == project_id), None)
    if idx is None:
        raise ProjectNotFoundError()
    projects.pop(idx)
