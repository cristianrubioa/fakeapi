from datetime import UTC
from datetime import datetime

from fastapi import HTTPException
from fastapi import status

from fakeapi.settings import settings
from fakeapi.storage import storage
from fakeapi.storage.base import WorkspaceData
from fakeapi.tasks.exceptions import ResourceNotFound
from fakeapi.tasks.models import TaskCreateModel
from fakeapi.tasks.models import TaskResponseModel
from fakeapi.tasks.models import TaskUpdateModel


def _tasks(workspace: WorkspaceData) -> list[dict]:
    return storage.get_resource(workspace.id, "tasks")


def get_tasks_list(workspace: WorkspaceData) -> list[TaskResponseModel]:
    return [TaskResponseModel(**t) for t in _tasks(workspace)]


def get_task_by_id(task_id: int, workspace: WorkspaceData) -> TaskResponseModel:
    task = next((t for t in _tasks(workspace) if t["id"] == task_id), None)
    if task is None:
        raise ResourceNotFound()
    return TaskResponseModel(**task)


def create_task(new_task: TaskCreateModel, workspace: WorkspaceData) -> TaskResponseModel:
    tasks = _tasks(workspace)
    limit = settings.PLANS[workspace.plan]["max_records_per_resource"]
    if len(tasks) >= limit:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Resource limit reached for this workspace.",
        )

    if new_task.user_id is not None:
        users = storage.get_resource(workspace.id, "users")
        if not any(u["id"] == new_task.user_id for u in users):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="user_id not found in workspace.",
            )

    if new_task.project_id is not None:
        projects = storage.get_resource(workspace.id, "projects")
        if not any(p["id"] == new_task.project_id for p in projects):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="project_id not found in workspace.",
            )

    new_id = max((t["id"] for t in tasks), default=0) + 1
    task_data = {
        "id": new_id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "user_id": new_task.user_id,
        "project_id": new_task.project_id,
        "created_at": datetime.now(UTC),
    }
    tasks.append(task_data)
    return TaskResponseModel(**task_data)


def update_task(task_id: int, new_task_data: TaskUpdateModel, workspace: WorkspaceData) -> TaskResponseModel:
    tasks = _tasks(workspace)
    task_dict = next((t for t in tasks if t["id"] == task_id), None)
    if task_dict is None:
        raise ResourceNotFound()
    task_dict.update(
        {
            "title": new_task_data.title,
            "description": new_task_data.description,
            "status": new_task_data.status,
            "user_id": new_task_data.user_id,
            "project_id": new_task_data.project_id,
        }
    )
    return TaskResponseModel(**task_dict)


def update_task_partial(task_id: int, task_updates: TaskUpdateModel, workspace: WorkspaceData) -> TaskResponseModel:
    tasks = _tasks(workspace)
    task_dict = next((t for t in tasks if t["id"] == task_id), None)
    if task_dict is None:
        raise ResourceNotFound()
    task_dict.update(task_updates.model_dump(exclude_unset=True))
    return TaskResponseModel(**task_dict)


def delete_task_by_id(task_id: int, workspace: WorkspaceData) -> None:
    tasks = _tasks(workspace)
    idx = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
    if idx is None:
        raise ResourceNotFound()
    tasks.pop(idx)
