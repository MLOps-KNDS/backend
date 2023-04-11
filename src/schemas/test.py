from pydantic import BaseModel
from datetime import datetime


class Test(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    created_by: int
    updated_at: datetime
    updated_by: int

    class Config:
        orm_mode = True
