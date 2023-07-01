from typing import Annotated
from pydantic import BaseModel, Field


class BaseGatePool(BaseModel):
    gate_id: Annotated[int, Field(description="Gate ID")]
    pool_id: Annotated[int, Field(description="Pool ID")]


class GatePoolPut(BaseGatePool):
    pass


class GatePoolDelete(BaseGatePool):
    pass


class GatePool(BaseGatePool):
    id: Annotated[int, Field(description="GatePool ID")]

    class Config:
        orm_mode = True
