from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field


class MlflowServerBase(BaseModel):
    name: Annotated[str, Field(description="MLflow server name")]
    tracking_uri: Annotated[str, Field(description="MLflow server tracking uri")]


class MlflowServerPatch(MlflowServerBase):
    name: Annotated[str | None, Field(description="MLflow server name")] = None
    description: Annotated[
        str | None, Field(description="MLflow server description")
    ] = None
    updated_by: Annotated[int, Field(description="User ID of the last updater")]


class MlflowServer(MlflowServerBase):
    id: Annotated[int, Field(description="MLflow server ID")]
    created_by: Annotated[int, Field(description="User ID of the creator")]
    created_at: Annotated[datetime, Field(description="Creation date")]
    updated_by: Annotated[int, Field(description="User ID of the last updater")]
    updated_at: Annotated[datetime, Field(description="Last update date")]

    class Config:
        orm_mode = True


class MlflowServerPut(MlflowServerBase):
    created_by: Annotated[int, Field(description="User ID of the creator")]
