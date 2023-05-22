from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime

from models.pool import PoolModelMode


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


class BasePoolModel(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]


class PoolPutModel(BasePoolModel):
    mode: Annotated[PoolModelMode, Field(description="Model mode")]


class PoolPatchModel(BasePoolModel):
    mode: Annotated[PoolModelMode | None, Field(description="Model mode")] = None


class PoolDeleteModel(BasePoolModel):
    pass


class PoolModelDetailed(BasePoolModel):
    name: Annotated[str, Field(description="Model name")]
    description: Annotated[str, Field(description="Model description")]
    mode: Annotated[PoolModelMode, Field(description="Model mode")]


class PoolModel(BasePoolModel):
    mode: Annotated[PoolModelMode, Field(description="Model mode")]

    class Config:
        orm_mode = True
