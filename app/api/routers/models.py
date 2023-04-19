from fastapi import APIRouter, Path, Body, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Optional

from api.schemas.model import Model

from api.utils.utility_functions import model_db, get_model_by_id


router = APIRouter(prefix="/api/models", tags=["models"])


class PatchModel(Model):
    """
    MLModel with all fields optional - for usage with patch request
    """

    __annotations__ = {
        field: Optional[field_type]
        for field, field_type in Model.__annotations__.items()
    }


@router.get("/")
async def get_models(
    skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 3
):
    """
    Allows retrieval of list of models from database

    :param skip: starting point to retrieve models from
    :param limit: how many models to retrieve
    :return: list of models
    """
    return list(model_db.values())[skip : skip + limit]


@router.get("/{model_id}")
async def get_single_model(model_id: Annotated[int, Path(title="id of model to get")]):
    """
    Allows retrieval of a model by it's designated id
    from database

    :param model_id: id of model to get
    :raises: HTTPException with status code 404 when
    model is not found
    :return: model
    """
    model = get_model_by_id(model_db, model_id)
    if not model:
        return JSONResponse(status_code=404, content={"message": "model not found"})
    return model


@router.patch("/{model_id}", response_model=Model)
async def update_model(
    model_id: Annotated[int, Path(title="id of model to update")],
    new_fields: Annotated[PatchModel, Body(description="fields of model to update")],
):
    """
    Allows updating a model by it's id

    :param model_id: id of model to update
    :param new_fields: JSON fields with new values to update a model
    :raises: HTTPException with status code 404 when
    model is not found
    :return: updated model
    """
    model = get_model_by_id(model_db, model_id)
    if not model:
        return JSONResponse(status_code=404, content={"message": "model not found"})
    update_data = new_fields.dict(exclude_unset=True)
    updated_model = model.copy(update=update_data)
    model_db[model_id] = updated_model
    updated_model_encoded = jsonable_encoder(updated_model)
    return JSONResponse(status_code=200, content=updated_model_encoded)


@router.post("/", status_code=201)
async def add_model_to_database(
    new_model: Annotated[Model, Body(description="model to add to database")],
):
    """
    Allows adding a new model to the database.
    If there exists a model in the database with the
    same id as the new model, the old model will be replaced,

    :param new_model: new model to add to database
    :return: newly added model
    """
    model_db[new_model.id] = new_model
    model_encoded = jsonable_encoder(new_model)
    return JSONResponse(status_code=201, content=model_encoded)
