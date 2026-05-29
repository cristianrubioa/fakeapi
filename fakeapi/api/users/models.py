from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from fakeapi.api.users.enums import UserRole


class UserBaseModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: UserRole = UserRole.MEMBER


class UserCreateModel(UserBaseModel):
    pass


class UserUpdateModel(UserBaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class UserResponseModel(UserBaseModel):
    id: int = Field(..., gt=0)
    created_at: datetime
