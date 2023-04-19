from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class Role(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    READER = "reader"
    WRITER = "writer"


class ResourceType(Enum):
    MODEL = "model"
    TEST = "test"
    POOL = "pool"


class BaseUser(BaseModel):
    name: Annotated[str, Field(description="User name")]
    surname: Annotated[str, Field(description="User surname")]
    email: Annotated[EmailStr, Field(description="User email")]


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseUser):
    id: Annotated[int, Field(description="User ID")]


class BaseUserRole(BaseModel):
    user_id: Annotated[int, Field(description="User ID")]
    resource_type: Annotated[ResourceType, Field(description="Resource type")]
    resource_id: Annotated[int, Field(description="Resource ID")]


class UserAddRole(BaseUserRole):
    role: Annotated[Role, Field(description="User role")]


class UserDeleteRole(BaseUserRole):
    pass
