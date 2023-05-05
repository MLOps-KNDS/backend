"""
This module contains the API routes and their corresponding
functions for handling pool-model-related requests.
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import (
    model as model_schemas,
    pool as pool_schemas,
)
from services import PoolService, get_db


router = APIRouter(prefix="/{pool_id}/model", tags=["pool-model"])


@router.get("/", response_model=model_schemas.Model, status_code=200)
async def get_pool_models(
    pool_id: int, db: Session = Depends(get_db)
):
    """
    Retrieves a list of models assigned to the pool with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :return: a list of model data
    """
    pass


@router.put("/{model_id}", response_model=pool_schemas.Pool, status_code=201)
async def put_pool_model(
    pool_id: int, model_id: int, db: Session = Depends(get_db)
):
    """
    Assigns a model to a pool.

    :param pool_id: pool ID
    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.

    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified model ID does not exist in the database.

    :return: the model data corresponding to the given ID
    """
    pass


@router.delete("/{model_id}", status_code=200)
async def delete_pool_model(
    pool_id: int, model_id: int, db: Session = Depends(get_db)
):
    """
    Unassigns a model from a pool.

    :param pool_id: pool ID
    :param model_id: model ID
    :param db: Database session

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.

    :raise HTTPException: 404 status code with "Model not found!" message
    if the specified model ID does not exist in the database.

    :return: a json with a "detail" key indicating success
    """
    pass
