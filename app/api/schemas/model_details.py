from typing import Annotated
from pydantic import BaseModel, Field


class ModelDetailsBase(BaseModel):
    artifact_uri: Annotated[str, Field(description="Path to the model artifact")]
    image_tag: Annotated[str, Field(description="Docker image tag")]
    replicas: Annotated[int, Field(description="Number of replicas")]
    cpu_request: Annotated[str, Field(description="CPU request")]
    cpu_limit: Annotated[str, Field(description="CPU limit")]
    memory_request: Annotated[str, Field(description="Memory request")]
    memory_limit: Annotated[str, Field(description="Memory limit")]


class PutModelDetails(ModelDetailsBase):
    model_id: Annotated[int, Field(description="Model ID")]
    pass


class PatchModelDetails(ModelDetailsBase):
    artifact_uri: Annotated[
        str | None, Field(description="Path to the model artifact")
    ] = None
    image_tag: Annotated[str | None, Field(description="Docker image tag")] = None
    replicas: Annotated[int | None, Field(description="Number of replicas")] = None
    cpu_request: Annotated[str | None, Field(description="CPU request")] = None
    cpu_limit: Annotated[str | None, Field(description="CPU limit")] = None
    memory_request: Annotated[str | None, Field(description="Memory request")] = None
    memory_limit: Annotated[str | None, Field(description="Memory limit")] = None


class ModelDetails(ModelDetailsBase):
    id: Annotated[int, Field(description="ModelDetails ID")]
    model_id: Annotated[int, Field(description="Model ID")]

    class Config:
        orm_mode = True
