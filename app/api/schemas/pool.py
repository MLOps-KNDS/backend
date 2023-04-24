from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field

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
