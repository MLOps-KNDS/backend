from pydantic import BaseModel, Field
from datetime import datetime


class Test(BaseModel):
    id: Field(int, description="Unique ID")
    name: Field(str, description="Test name")
    description: Field(str, description="Test description")
    created_at: Field(datetime, description="Test creation date")
    created_by: Field(int, description="User ID of the creator")
    updated_at: Field(datetime, description="Test update date")
    updated_by: Field(int, description="User ID of the last updater")

    class Config:
        orm_mode = True
