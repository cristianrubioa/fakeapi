from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from fakeapi.api.projects.enums import ProjectStatus


class ProjectBaseModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    status: ProjectStatus = ProjectStatus.ACTIVE


class ProjectCreateModel(ProjectBaseModel):
    pass


class ProjectUpdateModel(ProjectBaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    status: Optional[ProjectStatus] = None


class ProjectResponseModel(ProjectBaseModel):
    id: int = Field(..., gt=0)
    created_at: datetime
