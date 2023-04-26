from fastapi import APIRouter, Path, Body, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Annotated

from schemas import model as model_schemas
from services import model as model_services
from services.deps import get_db


router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("/", response_model=list[model_schemas.Model])
async def get_models(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 3,
    db: Session = Depends(get_db),
):
    """
    Allows retrieval of list of models from database

    :param skip: starting point to retrieve models from
    :param limit: how many models to retrieve
    :return: list of models
    """
    models = model_services.ModelService.get_models(db=db, skip=skip, limit=limit)
    return models


@router.get("/{model_id}", response_model=model_schemas.Model)
async def get_single_model(
    model_id: Annotated[int, Path(title="id of model to get")],
    db: Session = Depends(get_db),
):
    """
    Allows retrieval of a model by it's designated id
    from database

    :param model_id: id of model to get
    :raises: HTTPException with status code 404 when
    model is not found
    :return: model
    """
    model = model_services.ModelService.get_model_by_id(db=db, model_id=model_id)
    if not model:
        return JSONResponse(status_code=404, content={"message": "model not found"})
    return model


@router.patch("/{model_id}", response_model=model_schemas.Model)
async def update_model(
    model_id: Annotated[int, Path(title="id of model to update")],
    new_fields: Annotated[
        model_schemas.PatchModel, Body(description="fields of model to update")
    ],
    db: Session = Depends(get_db),
):
    """
    Allows updating a model by it's id

    :param model_id: id of model to update
    :param new_fields: JSON fields with new values to update a model
    model is not found
    :return: updated model
    """
    model = model_services.ModelService.get_model_by_id(db, model_id)
    if not model:
        return JSONResponse(status_code=404, content={"message": "model not found"})
    up_model = model_services.ModelService.patch_model(
        db=db, model_id=model_id, model=new_fields
    )
    up_model_encoded = jsonable_encoder(up_model)
    return JSONResponse(status_code=200, content=up_model_encoded)


@router.put("/", status_code=201, response_model=model_schemas.Model)
async def add_model_to_database(
    new_model: Annotated[
        model_schemas.PutModel, Body(description="model to add to database")
    ],
    db: Session = Depends(get_db),
):
    """
    Allows adding a new model to the database.
    If there exists a model in the database with the
    same id as the new model, the old model will be replaced,

    :param new_model: new model to add to database
    :param model_id: id of model to add/update
    :return: newly added model
    """
    db_model = model_services.ModelService.put_model(db=db, model=new_model)
    model_encoded = jsonable_encoder(db_model)
    return JSONResponse(status_code=201, content=model_encoded)


@router.delete("/{model_id}", status_code=200)
async def delete_model(
    model_id: Annotated[int, Path(title="id of model to delete")],
    db: Session = Depends(get_db),
):
    """
    Deletes model from database

    :param db: Database session
    :param model_id: id of model to delete
    :return: JSON response indicating successful deletion
    """
    if not model_services.ModelService.get_model_by_id(db=db, model_id=model_id):
        return JSONResponse(status_code=400, content={"message": "model not found"})
    return model_services.ModelService.delete_model(db=db, model_id=model_id)
