from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime

from schemas.commons import BaseEnum


class ModelMode(BaseEnum):
    PRODUCTION = "production"
    STAGING = "staging"


class BasePool(BaseModel):
    name: Annotated[str, Field(description="Pool name")]
    description: Annotated[str, Field(description="Pool description")]


class PoolPut(BasePool):
    created_by: Annotated[int, Field(description="User ID of the creator")]


class PoolPatch(BasePool):
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class Pool(BasePool):
    id: Annotated[int, Field(description="User ID")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]

    class Config:
        orm_mode = True


class PoolPostAddModel(BaseModel):
    model_id: Annotated[int, Field(description="Model ID")]
    mode: Annotated[ModelMode, Field(description="Model mode")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class PoolPostRemoveModel(BaseModel):
    model_id: Annotated[int, Field(description="Model ID")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class PoolPutModel(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    mode: Annotated[ModelMode, Field(description="Model mode")]


class PoolDeleteModel(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]


class PoolPatchModel(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    mode: Annotated[ModelMode | None, Field(description="Model mode")]


class PoolModel(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    mode: Annotated[ModelMode, Field(description="Model mode")]
