from datetime import UTC
from datetime import datetime

from fastapi import HTTPException
from fastapi import status

from fakeapi.settings import settings
from fakeapi.storage import storage
from fakeapi.storage.base import WorkspaceData
from fakeapi.users.exceptions import EmailAlreadyExistsError
from fakeapi.users.exceptions import UserNotFoundError
from fakeapi.users.models import UserCreateModel
from fakeapi.users.models import UserResponseModel
from fakeapi.users.models import UserUpdateModel


def _users(workspace: WorkspaceData) -> list[dict]:
    return storage.get_resource(workspace.id, "users")


def get_users_list(workspace: WorkspaceData) -> list[UserResponseModel]:
    return [UserResponseModel(**u) for u in _users(workspace)]


def get_user_by_id(user_id: int, workspace: WorkspaceData) -> UserResponseModel:
    user = next((u for u in _users(workspace) if u["id"] == user_id), None)
    if user is None:
        raise UserNotFoundError()
    return UserResponseModel(**user)


def create_user(new_user: UserCreateModel, workspace: WorkspaceData) -> UserResponseModel:
    users = _users(workspace)
    limit = settings.PLANS[workspace.plan]["max_records_per_resource"]
    if len(users) >= limit:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Resource limit reached for this workspace.",
        )

    if any(u["email"] == new_user.email for u in users):
        raise EmailAlreadyExistsError()

    new_id = max((u["id"] for u in users), default=0) + 1
    user_data = {
        "id": new_id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
        "created_at": datetime.now(UTC),
    }
    users.append(user_data)
    return UserResponseModel(**user_data)


def update_user(user_id: int, new_user_data: UserUpdateModel, workspace: WorkspaceData) -> UserResponseModel:
    users = _users(workspace)
    user_dict = next((u for u in users if u["id"] == user_id), None)
    if user_dict is None:
        raise UserNotFoundError()
    user_dict.update(
        {
            "name": new_user_data.name,
            "email": new_user_data.email,
            "role": new_user_data.role,
        }
    )
    return UserResponseModel(**user_dict)


def update_user_partial(user_id: int, user_updates: UserUpdateModel, workspace: WorkspaceData) -> UserResponseModel:
    users = _users(workspace)
    user_dict = next((u for u in users if u["id"] == user_id), None)
    if user_dict is None:
        raise UserNotFoundError()
    user_dict.update(user_updates.model_dump(exclude_unset=True))
    return UserResponseModel(**user_dict)


def delete_user_by_id(user_id: int, workspace: WorkspaceData) -> None:
    users = _users(workspace)
    idx = next((i for i, u in enumerate(users) if u["id"] == user_id), None)
    if idx is None:
        raise UserNotFoundError()
    users.pop(idx)
