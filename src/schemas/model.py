from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ModelStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Model(BaseModel):
    id: Field(int, description="Unique ID")
    name: Field(str, description="Model name")
    description: Field(str, description="Model description")
    created_at: Field(datetime, description="Model creation date")
    created_by: Field(int, description="User ID of the creator")
    updated_at: Field(datetime, description="Model update date")
    updated_by: Field(int, description="User ID of the last updater")
    image_tag: str = Field(None, description="Docker image tag")
    source_path: str = Field(None, description="Path to the model source code")
    status: ModelStatus = Field(
        ModelStatus.INACTIVE, description="Model status. Either active or inactive"
    )

    class Config:
        orm_mode = True


class ModelTest(BaseModel):
    id: Field(int, description="Unique ID")
    model_id: Field(int, description="Model ID")
    test_id: Field(int, description="Test ID")

    class Config:
        orm_mode = True
