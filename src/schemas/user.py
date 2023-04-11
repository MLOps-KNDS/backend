from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    READER = "reader"
    WRITER = "writer"


class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class ModelUserRole(BaseModel):
    id: int
    model_id: int
    user_id: int
    role: UserRole

    class Config:
        orm_mode = True


class PoolUserRole(BaseModel):
    id: int
    pool_id: int
    user_id: int
    role: UserRole

    class Config:
        orm_mode = True


class TestUserRole(BaseModel):
    id: int
    test_id: int
    user_id: int
    role: UserRole

    class Config:
        orm_mode = True
