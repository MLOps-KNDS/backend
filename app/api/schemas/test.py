from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime


class CreateTest(BaseModel):
    name: Annotated[str, Field(description="Test name")]
    description: Annotated[str, Field(description="Test description")]
    created_by: Annotated[int, Field(description="User ID of the creator")]


class UpdateTest(BaseModel):
    id: Annotated[int, Field(description="Test ID")]
    name: Annotated[str, Field(description="Test name")]
    description: Annotated[str, Field(description="Test description")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
