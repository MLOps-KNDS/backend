from fastapi import FastAPI, Query, Path, Body, HTTPException
from typing import Dict, Annotated
import datetime

from models.schemas import MLModel, PatchMLModel, get_model_by_id


app = FastAPI()

# Sample database for testing
db: Dict[int, MLModel] = {
    1: MLModel(
        id=1,
        name="model1",
        description="test description",
        created_at=datetime.datetime(2022, 7, 4, 21, 30, 57),
        created_by=1,
        updated_at=datetime.datetime(2022, 7, 6, 22, 50, 11),
        updated_by=12,
        image_tag="<img1>",
        source_path="/source/path/1",
        status="active",
    ),
    2: MLModel(
        id=2,
        name="model2",
        description="test description",
        created_at=datetime.datetime.now(),
        created_by=13,
        image_tag="<img2>",
        source_path="/source/path/2",
        status="active",
    ),
    3: MLModel(
        id=3,
        name="model3",
        created_at=datetime.datetime(2022, 7, 6, 22, 50, 12),
        created_by=1,
        updated_at=datetime.datetime.now(),
        updated_by=1,
        image_tag="<img3>",
        source_path="/source/path/3",
    ),
    4: MLModel(
        id=4,
        name="model4",
        created_at=datetime.datetime.now(),
        created_by=1,
        image_tag="<img4>",
        source_path="/source/path/4",
    ),
    5: MLModel(
        id=5,
        name="model5",
        created_at=datetime.datetime.now(),
        created_by=1,
        image_tag="<img5>",
        source_path="/source/path/5",
    ),
    6: MLModel(
        id=6,
        name="model6",
        description="test description",
        created_at=datetime.datetime.now(),
        created_by=124,
        image_tag="<img6>",
        source_path="/source/path/6",
        status="active",
    ),
}


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
    return list(db.values())[skip : skip + limit]


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


@app.patch("/api/models/{model_id}", response_model=MLModel)
async def update_model(
    model_id: Annotated[int, Path(title="id of model to update")],
    new_fields: Annotated[PatchMLModel, Body(description="fields of model to update")],
):
    """
    Allows updating a model by it's id

    :param model_id: id of model to update
    :param new_name: new name of model
    :param new_desc: new description od model
    :raises: HTTPException with status code 404 when
    model is not found
    :return: updated model
    """
    model = get_model_by_id(db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="model not found")
    update_data = new_fields.dict(exclude_unset=True)
    updated_model = model.copy(update=update_data)
    db[model_id] = updated_model
    return updated_model
