"""
This module contains the API routes and their corresponding
functions for handling model-related requests.
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import model as model_schemas
from services import ModelService, ModelDetailsService, get_db
from routers.model_details import router as model_details_router


router = APIRouter(prefix="/model", tags=["model"])
router.include_router(model_details_router)


@router.get("/{model_id}", response_model=model_schemas.Model, status_code=200)
async def get_model(model_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific model by ID.

    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified gate ID does not exist in the database.

    :return: the model data corresponding to the given ID
    """
    model = ModelService.get_model_by_id(db=db, model_id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found!")
    return model


@router.get("/", response_model=list[model_schemas.Model], status_code=200)
async def get_models(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieves a list of models with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified range of model ID's does not exist in the database.

    :return: a list of model data, where skip < model_id < limit
    """
    models = ModelService.get_models(db=db, skip=skip, limit=limit)
    if not models:
        raise HTTPException(status_code=404, detail="Models not found!")
    return models


@router.put("/", response_model=model_schemas.Model, status_code=201)
async def put_model(model_data: model_schemas.PutModel, db: Session = Depends(get_db)):
    """
    Creates a new model with the given information and returns the model information.

    :param model_data: the information of the new model to be created.
    :param db: Database session

    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name already exists in the database.

    :return: the newly-inserted model record
    """
    if ModelService.get_model_by_name(db=db, name=model_data.name):
        raise HTTPException(status_code=409, detail="Name already registered")
    result = ModelService.put_model(db=db, model=model_data)
    ModelDetailsService.put_model_details(db, result.id)
    return result


@router.patch("/{model_id}", response_model=model_schemas.Model, status_code=200)
async def patch_model(
    model_id: int,
    model_data: model_schemas.PatchModel,
    db: Session = Depends(get_db),
):
    """
    Allows updating a model by it's id

    :param model_id: id of model to update
    :param model_data: JSON fields with new values to update a model
    model is not found

    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified gate ID does not exist in the database.
    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name already exists in the database.

    :return: updated model
    """
    if not ModelService.get_model_by_id(db, model_id):
        raise HTTPException(status_code=404, detail="Model not found!")
    if ModelService.get_model_by_name(db=db, name=model_data.name):
        raise HTTPException(status_code=409, detail="Name already registered")
    return ModelService.patch_model(db=db, model_id=model_id, model=model_data)


@router.delete("/{model_id}", status_code=200)
async def delete_model(model_id: int, db: Session = Depends(get_db)):
    """
    Deletes the model with the given ID.

    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified gate ID does not exist in the database.

    :return: a json with a "detail" key indicating success
    """
    if not ModelService.get_model_by_id(db=db, model_id=model_id):
        raise HTTPException(status_code=404, detail="Model not found!")
    ModelDetailsService.delete_model_details(db, model_id)
    return ModelService.delete_model(db=db, model_id=model_id)
