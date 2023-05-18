from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field
from schemas.user import Role


class BaseGate(BaseModel):
    name: Annotated[str, Field(description="Gate name")]
    description: Annotated[str, Field(description="Gate surname")]


class GatePatch(BaseGate):
    name: Annotated[str | None, Field(description="Gate name")] = None
    description: Annotated[str | None, Field(description="Gate surname")] = None
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class Gate(BaseGate):
    id: Annotated[int, Field(description="Gate ID")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]

    class Config:
        orm_mode = True


class GatePut(BaseGate):
    created_by: Annotated[int, Field(description="User ID of the creator")]


class GatePatchAddPool(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class GatePatchRemovePool(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class GatePatchAddUser(BaseModel):
    user_id: Annotated[int, Field(description="User ID")]
    role: Annotated[Role, Field(description="User role")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class GatePatchRemoveUser(BaseModel):
    user_id: Annotated[int, Field(description="User ID")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
