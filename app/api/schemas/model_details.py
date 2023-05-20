from typing import Annotated
from pydantic import BaseModel, Field


class ModelDetailsBase(BaseModel):
    artifact_uri: Annotated[
        str | None, Field(description="Path to the model artifact")
    ] = None
    image_tag: Annotated[str | None, Field(description="Docker image tag")] = None
    replicas: Annotated[int | None, Field(description="Number of replicas")] = None
    cpu_request: Annotated[str | None, Field(description="CPU request")] = None
    cpu_limit: Annotated[str | None, Field(description="CPU limit")] = None
    memory_request: Annotated[str | None, Field(description="Memory request")] = None
    memory_limit: Annotated[str | None, Field(description="Memory limit")] = None


class ModelDetailsPatch(ModelDetailsBase):
    pass


class ModelDetails(ModelDetailsBase):
    id: Annotated[int, Field(description="ModelDetails ID")]
    model_id: Annotated[int, Field(description="Model ID")]

    class Config:
        orm_mode = True
