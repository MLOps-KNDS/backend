from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

from enum import Enum
from models.user import UserRole


class UserResourceType(Enum):
    MODEL = "model"
    TEST = "test"
    POOL = "pool"


class BaseUser(BaseModel):
    name: Annotated[str, Field(description="User name")]
    surname: Annotated[str, Field(description="User surname")]
    email: Annotated[EmailStr, Field(description="User email")]


class UserPut(BaseUser):
    pass


class UserPatch(BaseUser):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None


class User(BaseUser):
    id: Annotated[int, Field(description="User ID")]

    # here we have to implement the class that represents the
    # User class in models.user module

    class Config:
        orm_mode = True


class BaseUserRole(BaseModel):
    user_id: Annotated[int, Field(description="User ID")]
    resource_type: Annotated[UserResourceType, Field(description="Resource type")]
    resource_id: Annotated[int, Field(description="Resource ID")]


class UserPatchRole(BaseUserRole):
    role: Annotated[UserRole, Field(description="User role")]


class UserDeleteRole(BaseUserRole):
    pass
