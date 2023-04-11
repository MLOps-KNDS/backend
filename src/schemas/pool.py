from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class PoolModelMode(Enum):
    PRODUCTION = "production"
    STAGING = "staging"


class Pool(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    created_by: int
    updated_at: datetime
    updated_by: int

    class Config:
        orm_mode = True


class PoolModel(BaseModel):
    id: int
    pool_id: int
    model_id: int
    mode: PoolModelMode

    class Config:
        orm_mode = True
