"""
This is the main module.

It contains the FastAPI app.
"""

from fastapi import FastAPI, HTTPException
from models.model import MLModel
from typing import List
from uuid import uuid4, UUID
app = FastAPI()

# Example data
models_from_db: List[MLModel] = [
    MLModel(id=uuid4(), name="Logistic Regression", description="Binary classification model", created_by=123, updated_by=456, image_tag="v1.0", source_path="/path/to/source"),
    MLModel(id=uuid4(), name="Random Forest", description="Ensemble model for classification and regression", created_by=789, updated_by=123, image_tag="v2.0", source_path="/path/to/source"),
    MLModel(id=uuid4(), name="Support Vector Machine", description="Linear model for classification and regression", created_by=456, updated_by=789, image_tag="v1.1", source_path="/path/to/source"),
    MLModel(id=uuid4(), name="K-Nearest Neighbors", description="Non-parametric model for classification and regression", created_by=123, updated_by=456, image_tag="v1.2", source_path="/path/to/source"),
    MLModel(id=uuid4(), name="Naive Bayes", description="Probabilistic model for classification", created_by=789, updated_by=123, image_tag="v2.1", source_path="/path/to/source"),
    MLModel(id=uuid4(), name="Decision Tree", description="Tree-based model for classification and regression", created_by=456, updated_by=789, image_tag="v1.3", source_path="/path/to/source"),
    MLModel(id=uuid4(), name="Gradient Boosting", description="Ensemble model for classification and regression", created_by=123, updated_by=456, image_tag="v1.4", source_path="/path/to/source"),
    MLModel(id=uuid4(), name="Neural Network", description="Deep learning model for classification and regression", created_by=789, updated_by=123, image_tag="v2.2", source_path="/path/to/source")
]


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.

    :return: A "Server ON" message.
    """
    return {"Server": "ON"}


@app.get("/api/models")
async def fetch_models() -> List[MLModel]:
    """
    Display all ML Models.

    :return: All ML Models.
    :rtype: List[MLModel]
    """
    return models_from_db


@app.get("/api/models/{id}")
async def fetch_model_by_id(id: UUID) -> MLModel:
    """
    Display the single model indicated by id.

    :param id: ID of specified ML Model
    :type id: UUID

    :raises HTTPException: If the value of id does not match any model.

    :return: ML Model with given id.
    :rtype: MLModel
    """
    for model in models_from_db:
        if model.id == id:
            return model
    raise HTTPException(status_code=404, detail="Model not found")


@app.get("/api/models/")
async def fetch_model_skip_limit(skip: int, limit: int) -> List[MLModel]:
    """
    Display the models indicated by skip and limit values.

    :param skip: Do not display [skip value] first models.
    :type skip: int
    :param limit: Display [limit value] models after skip.
    :type limit: int

    :return: Models indicated by skip and limit values.
    :rtype: List[MLModel]
    """
    return models_from_db[skip:skip+limit]


@app.patch("/api/models/{id}")
async def update_model(id: UUID, updates: dict) -> MLModel:
    """
    Update one or more field of indicated model.

    :param id: ID of model which will be updated.
    :type id: UUID
    :param updates: Model or only few fields of model which were updated.
    :type updates: dict

    :raises HTTPException: If the value of id does not match any model.

    :return: Updated model.
    :rtype: MLModel
    """
    index: int = -1
    for i, ml in enumerate(models_from_db):
        if ml.id == id:
            index = i
    if index < 0:
        raise HTTPException(status_code=404, detail="Model not found")
    models_from_db[index].update(updates)
    return models_from_db[index]
