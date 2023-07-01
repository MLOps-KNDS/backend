from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field


class BaseTest(BaseModel):
    name: Annotated[str, Field(description="Test name")]
    description: Annotated[str, Field(description="Test description")]


class TestPut(BaseTest):
    pass


class TestPatch(BaseTest):
    name: Annotated[str | None, Field(description="Test name")] = None
    description: Annotated[str | None, Field(description="Test description")] = None


class Test(BaseTest):
    id: Annotated[int, Field(description="Test ID")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]

    class Config:
        orm_mode = True
