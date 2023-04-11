from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    READER = "reader"
    WRITER = "writer"


class User(BaseModel):
    id: Field(int, description="Unique ID")
    name: Field(str, description="User name")
    surname: Field(str, description="User surname")
    email: Field(EmailStr, description="User email")

    class Config:
        orm_mode = True


class ModelUserRole(BaseModel):
    id: Field(int, description="Unique ID")
    model_id: Field(int, description="Model ID")
    user_id: Field(int, description="User ID")
    role: Field(
        UserRole, description="User's role. Either owner, admin, reader or writer"
    )

    class Config:
        orm_mode = True


class PoolUserRole(BaseModel):
    id: Field(int, description="Unique ID")
    pool_id: Field(int, description="Pool ID")
    user_id: Field(int, description="User ID")
    role: Field(
        UserRole, description="User's role. Either owner, admin, reader or writer"
    )

    class Config:
        orm_mode = True


class TestUserRole(BaseModel):
    id: int
    test_id: int
    user_id: int
    role: UserRole

    class Config:
        orm_mode = True
