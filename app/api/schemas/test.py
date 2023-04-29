from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field


class BaseTest(BaseModel):
    name: Annotated[str, Field(description="Test name")]
    description: Annotated[str, Field(description="Test description")]


class TestPut(BaseTest):
    created_by: Annotated[int, Field(description="User ID of the creator")]


class TestPatch(BaseTest):
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class Test(BaseTest):
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]

    class Config:
        orm_mode = True
