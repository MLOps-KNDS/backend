from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PoolModelMode(Enum):
    PRODUCTION = "production"
    STAGING = "staging"


class Pool(BaseModel):
    id: Field(int, description="Unique ID")
    name: Field(str, description="Pool name")
    description: Field(str, description="Pool description")
    created_at: Field(datetime, description="Pool creation date")
    created_by: Field(int, description="User ID of the creator")
    updated_at: Field(datetime, description="Pool update date")
    updated_by: Field(int, description="User ID of the last updater")

    class Config:
        orm_mode = True


class PoolModel(BaseModel):
    id: Field(int, description="Unique ID")
    pool_id: Field(int, description="Pool ID")
    model_id: Field(int, description="Model ID")
    mode: Field(PoolModelMode, description="Model's Mode. Either production or staging")

    class Config:
        orm_mode = True
