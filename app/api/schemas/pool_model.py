from typing import Annotated
from pydantic import BaseModel, Field

from models.pool import PoolModelMode


class BasePoolModel(BaseModel):
    mode: Annotated[PoolModelMode, Field(description="Model mode")]
    weight: Annotated[int, Field(description="Model weight")]


class PoolPutModel(BasePoolModel):
    pass


class PoolPatchModel(BasePoolModel):
    mode: Annotated[PoolModelMode | None, Field(description="Model mode")] = None
    weight: Annotated[int | None, Field(description="Model weight")] = None


class PoolModelDetailed(BasePoolModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    name: Annotated[str, Field(description="Model name")]
    description: Annotated[str, Field(description="Model description")]


class PoolModel(BasePoolModel):
    pool_id: Annotated[int, Field(description="Pool ID")]
    model_id: Annotated[int, Field(description="Model ID")]

    class Config:
        orm_mode = True
