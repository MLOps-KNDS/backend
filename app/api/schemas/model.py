from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CreateModel(BaseModel):
    name: Annotated[str, Field(description="Model name")]
    description: Annotated[str, Field(description="Model description")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    source_path: Annotated[str, Field(description="Path to the model source code")]
    status: Annotated[Status, Field(description="Model status")]


class UpdateModel(BaseModel):
    id: Annotated[int, Field(description="Model ID")]
    name: Annotated[str, Field(description="Model name")]
    description: Annotated[str, Field(description="Model description")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    source_path: Annotated[str, Field(description="Path to the model source code")]
    status: Annotated[Status, Field(description="Model status")]
