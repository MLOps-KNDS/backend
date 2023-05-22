from typing import Annotated
from pydantic import BaseModel, Field

from models.pool import PoolModelMode


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
