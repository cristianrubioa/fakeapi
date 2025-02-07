from datetime import datetime

from pydantic import BaseModel, Field

from fakeapi.settings import settings
from fakeapi.tasks.enums import TaskStatus


class TaskModel(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(
        ...,
        min_length=settings.TITLE_LIMITS["min"],
        max_length=settings.TITLE_LIMITS["max"],
    )
    description: str = Field(
        ...,
        min_length=settings.DESCRIPTION_LIMITS["min"],
        max_length=settings.DESCRIPTION_LIMITS["max"],
    )
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
