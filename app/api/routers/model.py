"""
This module contains the API routes and their corresponding
functions for handling model-related requests.
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
import asyncio

from schemas import model as model_schemas
from models.model import ModelStatus
from services import ModelService, ModelDetailsService, get_db
from routers.model_details import router as model_details_router
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decode_jwt_token


router = APIRouter(prefix="/model", tags=["model"], dependencies=[Depends(JWTBearer())])
router.include_router(model_details_router)

_logger = logging.getLogger(__name__)


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
    return models


@router.put("/", response_model=model_schemas.Model, status_code=201)
async def put_model(
    model_data: model_schemas.ModelPut,
    db: Session = Depends(get_db),
    credentials=Depends(JWTBearer()),
):
    """
    Creates a new model with the given information and returns the model information.

    :param model_data: the information of the new model to be created.
    :param db: Database session

    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name already exists in the database.

    :return: the newly-inserted model record
    """
    payload = decode_jwt_token(credentials)
    user_id = payload.get("user_id")
    if ModelService.get_model_by_name(db=db, name=model_data.name):
        raise HTTPException(status_code=409, detail="Name already registered")
    result = ModelService.put_model(db=db, model=model_data, user_id=user_id)
    ModelDetailsService.put_model_details(db, result.id)
    return result


@router.post("/{model_id}/deploy", status_code=200)
async def deploy_model(
    model_id: int,
    db: Session = Depends(get_db),
):
    """
    Activates the model with the given ID.

    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Model not found!"
    :raise HTTPException: 409 status code with "Model already active!"
    :raise HTTPException: 404 status code with "Model details not found!"
    :raise HTTPException: 406 status code with "Model details are not complete!"

    :return: a json with a "detail" key indicating success
    """
    db_model = ModelService.get_model_by_id(db=db, model_id=model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found!")

    db_model_details = ModelDetailsService.get_model_details_by_model_id(db, model_id)
    if not db_model_details:
        raise HTTPException(status_code=404, detail="Model details not found!")

    for item in db_model_details.__dict__.items():
        if item[0] in ["cpu_utilization", "memory_utilization", "max_replicas"]:
            continue
        if item[1] is None:
            raise HTTPException(
                status_code=406, detail="Model details are not complete!"
            )
    if (
        db_model_details.cpu_utilization or db_model_details.memory_utilization
    ) and not db_model_details.max_replicas:
        raise HTTPException(status_code=406, detail="Model details are not complete!")

    asyncio.create_task(
        ModelService.deploy_model(
            db=db,
            name=db_model.name,
            model_details=db_model_details,
        )
    )
    return JSONResponse({"detail": "Deploy started!"})


@router.post("/{model_id}/deactivate", status_code=200)
async def deactivate_model(model_id: int, db: Session = Depends(get_db)):
    """
    Deactivates the model with the given ID.

    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Model not found!" message
    :raise HTTPException: 409 status code with "Model already inactive!" message

    :return: a json with a "detail" key indicating success
    """
    model = ModelService.get_model_by_id(db=db, model_id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found!")
    if model.status == ModelStatus.INACTIVE:
        raise HTTPException(status_code=409, detail="Model already inactive!")

    asyncio.create_task(
        ModelService.deactivate_model(db=db, model_id=model_id, name=model.name)
    )
    return JSONResponse({"detail": "Deactivation started!"})


@router.patch("/{model_id}", response_model=model_schemas.Model, status_code=200)
async def patch_model(
    model_id: int,
    model_data: model_schemas.ModelPatch,
    db: Session = Depends(get_db),
    credentials: str = Depends(JWTBearer()),
):
    """
    Allows updating a model by it's id

    :param model_id: id of model to update
    :param model_data: JSON fields with new values to update a model
    model is not found
    :param db: Database session
    :param credentials: JWT token

    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified gate ID does not exist in the database.
    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name already exists in the database.

    :return: updated model
    """
    payload = decode_jwt_token(credentials)
    user_id = payload.get("user_id")
    if not ModelService.get_model_by_id(db, model_id):
        raise HTTPException(status_code=404, detail="Model not found!")
    if ModelService.get_model_by_name(db=db, name=model_data.name):
        raise HTTPException(status_code=409, detail="Name already registered")
    return ModelService.patch_model(
        db=db, model_id=model_id, model=model_data, user_id=user_id
    )


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


@router.post("/{model_id}/build", status_code=200)
async def build_model(model_id: int, db: Session = Depends(get_db)):
    """
    Builds container of the model with the given ID.

    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Model not found!"
    :raise HTTPException: 404 status code with "Model details not found!"
    :raise HTTPException: 406 status code with "Model details are not complete!"

    :return: a json with a "detail" key indicating success
    """
    db_model = ModelService.get_model_by_id(db=db, model_id=model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found!")

    db_model_details = ModelDetailsService.get_model_details_by_model_id(db, model_id)
    if not db_model_details:
        raise HTTPException(status_code=404, detail="Model details not found!")

    if db_model_details.artifact_uri is None:
        raise HTTPException(status_code=406, detail="No artifact URI specified!")

    asyncio.create_task(
        ModelService.build_model(
            db=db,
            name=db_model.name,
            model_details=db_model_details,
        )
    )
    return JSONResponse({"detail": "Build started!"})
