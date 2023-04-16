from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    READER = "reader"
    WRITER = "writer"


class User(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    name: Annotated[str, Field(description="User name")]
    surname: Annotated[str, Field(description="User surname")]
    email: Annotated[EmailStr, Field(description="User email")]

    class Config:
        orm_mode = True


class ModelUserRole(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    user_id: Annotated[int, Field(description="User ID")]
    role: Annotated[
        UserRole,
        Field(description="User's role. Either owner, admin, reader or writer"),
    ]

    class Config:
        orm_mode = True


class PoolUserRole(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    pool_id: Annotated[int, Field(description="Pool ID")]
    user_id: Annotated[int, Field(description="User ID")]
    role: Annotated[
        UserRole,
        Field(description="User's role. Either owner, admin, reader or writer"),
    ]

    class Config:
        orm_mode = True


class TestUserRole(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    test_id: Annotated[int, Field(description="Test ID")]
    user_id: Annotated[int, Field(description="User ID")]
    role: Annotated[
        UserRole,
        Field(description="User's role. Either owner, admin, reader or writer"),
    ]

    class Config:
        orm_mode = True
