from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime


class BasePool(BaseModel):
    name: Annotated[str, Field(description="Pool name")]
    description: Annotated[str, Field(description="Pool description")]


class PoolPut(BasePool):
    pass


class PoolPatch(BasePool):
    name: Annotated[str | None, Field(description="Pool name")] = None
    description: Annotated[str | None, Field(description="Pool description")] = None


class Pool(BasePool):
    id: Annotated[int, Field(description="User ID")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]

    class Config:
        orm_mode = True
