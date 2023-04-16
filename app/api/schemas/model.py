from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ModelStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Model(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    name: Annotated[str, Field(description="Model name")]
    description: Annotated[str, Field(description="Model description")]
    created_at: Annotated[datetime, Field(description="Model creation date")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    updated_at: Annotated[datetime, Field(description="Model update date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    image_tag: str = Annotated[None, Field(description="Docker image tag")]
    source_path: str = Annotated[
        None, Field(description="Path to the model source code")
    ]
    status: ModelStatus = Annotated[
        ModelStatus.INACTIVE,
        Field(description="Model status. Either active or inactive"),
    ]

    class Config:
        orm_mode = True


class ModelTest(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    model_id: Annotated[int, Field(description="Model ID")]
    test_id: Annotated[int, Field(description="Test ID")]

    class Config:
        orm_mode = True
