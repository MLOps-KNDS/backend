from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field


class BaseGate(BaseModel):
    name: Annotated[str, Field(description="Gate name")]
    description: Annotated[str, Field(description="Gate surname")]


class GatePatch(BaseGate):
    name: Annotated[str | None, Field(description="Gate name")] = None
    description: Annotated[str | None, Field(description="Gate surname")] = None


class Gate(BaseGate):
    id: Annotated[int, Field(description="Gate ID")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]

    class Config:
        orm_mode = True


class GatePut(BaseGate):
    pass
