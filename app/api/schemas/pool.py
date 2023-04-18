from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field


class ModelMode(Enum):
    PRODUCTION = "production"
    STAGING = "staging"


class CreatePool(BaseModel):
    name: Annotated[str, Field(description="Pool name")]
    description: Annotated[str, Field(description="Pool description")]
    created_by: Annotated[int, Field(description="User ID of the creator")]


class UpdatePool(BaseModel):
    id: Annotated[int, Field(description="Pool ID")]
    name: Annotated[str, Field(description="Pool name")]
    description: Annotated[str, Field(description="Pool description")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class PoolAddModel(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    mode: Annotated[ModelMode, Field(description="Model mode")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class PoolRemoveModel(BaseModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
