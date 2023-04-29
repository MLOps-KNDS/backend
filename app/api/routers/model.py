"""
This module contains the API routes and their corresponding
functions for handling user-related requests.
"""

from fastapi import APIRouter, Path, Body, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Annotated

from schemas import model as model_schemas
from services import ModelService, get_db


router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=list[model_schemas.Model])
async def get_models(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieves a list of models with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :return: a list of model data, where skip <= model_id < skip + limit
    """
    models = ModelService.get_models(db=db, skip=skip, limit=limit)
    return models


@router.get("/{model_id}", response_model=model_schemas.Model)
async def get_single_model(
    model_id: Annotated[int, Path(title="id of model to get")],
    db: Session = Depends(get_db),
):
    """
    Retrieves the information of a specific model by ID.

    :param model_id: model ID
    :param db: Database session

    :return: the model data corresponding to the given ID or a message with status code
    404 indicating that the model was not found
    """
    model = ModelService.get_model_by_id(db=db, model_id=model_id)
    if not model:
        return JSONResponse(status_code=404, content={"message": "model not found"})
    return model


@router.patch("/{model_id}", status_code=200, response_model=model_schemas.Model)
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
    model = ModelService.get_model_by_id(db, model_id)
    if not model:
        return JSONResponse(status_code=404, content={"message": "model not found"})
    return ModelService.patch_model(db=db, model_id=model_id, model=new_fields)


@router.put("/", status_code=201, response_model=model_schemas.Model)
async def add_model_to_database(
    new_model: Annotated[
        model_schemas.PutModel, Body(description="model to add to database")
    ],
    db: Session = Depends(get_db),
):
    """
    Creates a new model with the given information and returns the model information.

    :param new_model: the information of the new model to be created.
    :param db: Database session

    :return: the newly-inserted model record
    """
    db_model = ModelService.put_model(db=db, model=new_model)
    model_encoded = jsonable_encoder(db_model)
    return JSONResponse(content=model_encoded)


@router.delete("/{model_id}", status_code=200)
async def delete_model(
    model_id: Annotated[int, Path(title="id of model to delete")],
    db: Session = Depends(get_db),
):
    """
    Deletes the model with the given ID.

    :param model_id: model ID
    :param db: Database session

    :return: a json with a "detail" key indicating success
    """
    if not ModelService.get_model_by_id(db=db, model_id=model_id):
        return JSONResponse(status_code=404, content={"message": "model not found"})
    return ModelService.delete_model(db=db, model_id=model_id)
