from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ModelStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Model(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    created_by: int
    updated_at: datetime
    updated_by: int
    image_tag: str = None
    source_path: str = None
    status: ModelStatus = ModelStatus.INACTIVE

    class Config:
        orm_mode = True


class ModelTest(BaseModel):
    id: int
    model_id: int
    test_id: int

    class Config:
        orm_mode = True
