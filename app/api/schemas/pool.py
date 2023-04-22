from typing import Annotated
from pydantic import BaseModel, Field

from schemas.commons import BaseEnum


class ModelMode(BaseEnum):
    PRODUCTION = "production"
    STAGING = "staging"


class BasePool(BaseModel):
    name: Annotated[str, Field(description="Pool name")]
    description: Annotated[str, Field(description="Pool description")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class PoolPut(BasePool):
    pass


class PoolPatch(BasePool):
    name: str | None = None
    description: str | None = None
    updated_by: int


class Pool(BasePool):
    id: Annotated[int, Field(description="User ID")]

    class Config:
        orm_mode = True


class PoolPostAddModel(BaseModel):
    model_id: Annotated[int, Field(description="Model ID")]
    mode: Annotated[ModelMode, Field(description="Model mode")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class PoolPostRemoveModel(BaseModel):
    model_id: Annotated[int, Field(description="Model ID")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
