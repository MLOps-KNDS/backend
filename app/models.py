from typing import List
from enum import Enum
from pydantic import BaseModel


class ModelStatus(Enum):
    active = "active"
    inactive = "inactive"


class MLModel(BaseModel):
    id: int
    name: str
    status: ModelStatus = ModelStatus.inactive
    description: str | None = None


def get_model_by_id(database: List[MLModel], model_id: int) -> MLModel | None:
    """
    Simple function to get model by id from the sample database

    :param database: database to get model from
    :param model_id: id of model to get
    :return: model if id was in database or None if wasn't
    """
    for model in database:
        if model.id == model_id:
            return model
