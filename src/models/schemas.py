from typing import Dict, Optional
from enum import Enum
import datetime

from pydantic import BaseModel


class ModelStatus(Enum):
    active = "active"
    inactive = "inactive"


class MLModel(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime.datetime
    created_by: int
    updated_at: datetime.datetime | None = None
    updated_by: int | None = None
    image_tag: str
    source_path: str
    status: ModelStatus = ModelStatus.inactive


class PatchMLModel(MLModel):
    """
    MLModel with all fields optional - for usage with patch request
    """

    __annotations__ = {
        field: Optional[field_type]
        for field, field_type in MLModel.__annotations__.items()
    }


def get_model_by_id(database: Dict[int, MLModel], model_id: int) -> MLModel | None:
    """
    Simple function to get model by id from the sample database

    :param database: database to get model from
    :param model_id: id of model to get
    :return: model if id was in database or None if wasn't
    """
    model = database.get(model_id)

    return model

