from fastapi import FastAPI, Query, Path, HTTPException
from typing import List, Annotated

from models import MLModel, get_model_by_id

app = FastAPI()


db: List[MLModel] = [
    MLModel(id=1, name="model1", description="test description", status="active"),
    MLModel(id=2, name="model2", description="test description second"),
    MLModel(id=3, name="model3"),
    MLModel(id=4, name="model4"),
    MLModel(id=5, name="model5", description="test description fifth"),
]


@app.get("/api/status")
async def get_status():
    """
    Simple function that allows one to check if the server is running

    :return: ok status if server is running
    """
    return {"status": "OK"}


@app.get("/api/models/")
async def get_models(
    skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 3
):
    """
    Allows retrieval of list of models from database

    :param skip: starting point to retrieve models from
    :param limit: how many models to retrieve
    :return: list of models
    """
    return db[skip : skip + limit]


@app.get("/api/models/{model_id}")
async def get_single_model(model_id: Annotated[int, Path(title="id of model to get")]):
    """
    Allows retrieval of a model by it's designated id
    from database

    :param model_id: id of model to get
    :raises: HTTPException with status code 404 when
    model is not found
    :return: model
    """
    model = get_model_by_id(db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="model not found")
    return model


@app.patch("/api/models/{model_id}")
async def update_model(
    model_id: Annotated[int, Path(title="id of model to update")],
    new_name: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
    new_desc: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
):
    """
    Allows updating a model by giving it's id

    :param model_id: id of model to update
    :param new_name: new name of model
    :param new_desc: new description od model
    :raises: HTTPException with status code 404 when
    model is not found
    :return: updated model
    """
    model = get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="model not found")

    if new_name:
        model.name = new_name
    if new_desc:
        model.description = new_desc

    return model
