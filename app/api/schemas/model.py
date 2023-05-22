from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime

from models.model import ModelStatus


class ModelBase(BaseModel):
    name: Annotated[str, Field(description="Model name")]
    description: Annotated[str, Field(description="Model description")]


class ModelPut(ModelBase):
    created_by: Annotated[int, Field(description="User ID of the creator")]


class ModelPatch(ModelBase):
    name: Annotated[str | None, Field(description="Model name")] = None
    description: Annotated[str | None, Field(description="Model description")] = None
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class Model(ModelBase):
    id: Annotated[int, Field(description="Model ID")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]
    status: Annotated[ModelStatus, Field(description="Model status")]

    class Config:
        orm_mode = True


class ModelTest(BaseModel):
    id: Annotated[int, Field(description="ModelTest ID")]
    model_id: Annotated[int, Field(description="Model id")]
    user_id: Annotated[int, Field(description="User id")]
