from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PoolModelMode(Enum):
    PRODUCTION = "production"
    STAGING = "staging"


class Pool(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    name: Annotated[str, Field(description="Pool name")]
    description: Annotated[str, Field(description="Pool description")]
    created_at: Annotated[datetime, Field(description="Pool creation date")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    updated_at: Annotated[datetime, Field(description="Pool update date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]

    class Config:
        orm_mode = True


class PoolModel(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    mode: Annotated[
        PoolModelMode, 
        Field(description="Model's Mode. Either production or staging")
    ]

    class Config:
        orm_mode = True
