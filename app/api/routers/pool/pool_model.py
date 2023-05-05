"""
This module contains the API routes and their corresponding
functions for handling pool-model-related requests.
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import pool as pool_schemas
from services import PoolService, get_db


router = APIRouter(prefix="/{pool_id}/model", tags=["pool-model"])


@router.get("/{model_id}")
async def get_pool_model(pool_id: int, model_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific model in pool by ID.

    :param pool_id: pool ID
    :param db: Database session

    :return: the model data corresponding to the given ID

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    """
    pass


@router.get("/")
async def get_pool_models(pool_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a list of models with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :return: a list of pool data, where skip <= pool_id < skip + limit
    """
    pass


@router.put("/")
async def put_pool_model(pool_id: int, db: Session = Depends(get_db)):
    """
    Creates a new model in pool with the given information
    and returns the model information.

    :param pool_id: pool ID
    :param db: Database session

    :return: the newly-inserted model record

    :raise HTTPException: 400 status code with "Name already registered"
    message if the provided name already exists in the database.
    """
    pass


@router.patch("/{model_id}")
async def patch_pool_model(pool_id: int, model_id: int, db: Session = Depends(get_db)):
    """
    Updates the information of an existing model in pool with the provided data and
    returns the updated model information.

    :param pool_id: pool ID
    :param db: Database session

    :return: the updated model record

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    """
    pass


@router.delete("/{model_id}")
async def delete_pool_model(pool_id: int, model_id: int, db: Session = Depends(get_db)):
    """
    Deletes the model in pool with the given ID.

    :param pool_id: pool ID
    :param db: Database session

    :return: a json with a "detail" key indicating success
    """
    pass
