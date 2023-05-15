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
    pass


class PatchModelDetails(ModelDetailsBase):
    pass


class ModelDetails(ModelDetailsBase):
    id: Annotated[int, Field(description="ModelDetails ID")]

    class Config:
        orm_mode = True
