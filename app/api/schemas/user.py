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


class AddUser(BaseModel):
    name: Annotated[str, Field(description="User name")]
    surname: Annotated[str, Field(description="User surname")]
    email: Annotated[EmailStr, Field(description="User email")]


class UpdateUser(BaseModel):
    id: Annotated[int, Field(description="User ID")]
    name: Annotated[str, Field(description="User name")]
    surname: Annotated[str, Field(description="User surname")]
    email: Annotated[EmailStr, Field(description="User email")]


class UserAddRole(BaseModel):
    user_id: Annotated[int, Field(description="User ID")]
    role: Annotated[Role, Field(description="User role")]
    resource_type: Annotated[ResourceType, Field(description="Resource type")]
    resource_id: Annotated[int, Field(description="Resource ID")]


class UserDeleteRole(BaseModel):
    user_id: Annotated[int, Field(description="User ID")]
    resource_type: Annotated[ResourceType, Field(description="Resource type")]
    resource_id: Annotated[int, Field(description="Resource ID")]
