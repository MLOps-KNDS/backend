from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from enum import Enum, EnumMeta


#  creates possibility to do for example:  if "owner" in Role
class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class Role(BaseEnum):
    OWNER = "owner"
    ADMIN = "admin"
    READER = "reader"
    WRITER = "writer"


class ResourceType(BaseEnum):
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
    email: EmailStr
    new_email: EmailStr | None = None


class User(BaseUser):
    id: Annotated[int, Field(description="User ID")]

    # here we have to implement the class that represents the
    # User class in models.user module

    class Config:
        orm_mode = True


class BaseUserRole(BaseModel):
    user_id: Annotated[int, Field(description="User ID")]
    resource_type: Annotated[ResourceType, Field(description="Resource type")]
    resource_id: Annotated[int, Field(description="Resource ID")]


class UserPatchRole(BaseUserRole):
    role: Annotated[Role, Field(description="User role")]


class UserDeleteRole(BaseUserRole):
    pass
