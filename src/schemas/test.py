from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime


class Test(BaseModel):
    id: Annotated[int, Field(description="Unique ID")]
    name: Annotated[str, Field(description="Test name")]
    description: Annotated[str, Field(description="Test description")]
    created_at: Annotated[datetime, Field(description="Test creation date")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    updated_at: Annotated[datetime, Field(description="Test update date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]

    class Config:
        orm_mode = True
