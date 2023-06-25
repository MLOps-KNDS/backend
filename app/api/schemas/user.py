from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


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

    class Config:
        orm_mode = True
