"""
This module contains the API routes and their corresponding
functions for handling user-related requests.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import pool as pool_schemas
from services import get_db, PoolService


router = APIRouter(prefix="/pool", tags=["pool"])


@router.get("/", response_model=list[pool_schemas.Pool])
def get_pools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of pools with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :return: a list of pool data, where skip <= pool_id < skip + limit
    """
    return PoolService.get_pools(skip=skip, limit=limit, db=db)


@router.get("/{pool_id}", response_model=pool_schemas.Pool)
def get_pool(pool_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific pool by ID.

    :param pool_id: pool ID
    :param db: Database session

    :return: the pool data corresponding to the given ID

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    """
    pool = PoolService.get_pool_by_id(db=db, id=pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found!")
    return pool


@router.put("/", response_model=pool_schemas.Pool)
def put_pool(pool_data: pool_schemas.PoolPut, db: Session = Depends(get_db)):
    """
    Creates a new pool with the given information and returns the pool information.

    :param pool_data: the information of the new pool to be created.
    :param db: Database session

    :return: the newly-inserted pool record

    :raise HTTPException: 400 status code with "Name already registered"
    message if the provided name already exists in the database.
    """
    if PoolService.get_pool_by_name(db=db, name=pool_data.name):
        raise HTTPException(status_code=400, detail="Name already registered")
    return PoolService.put_pool(db=db, pool_data=pool_data)


@router.patch("/{user_id}", response_model=pool_schemas.Pool)
def patch_pool(
    pool_id: int, pool_data: pool_schemas.PoolPatch, db: Session = Depends(get_db)
):
    """
    Updates the information of an existing pool with the provided data and
    returns the updated pool information.

    :param pool_data: the information of the new pool to be created.
    :param db: Database session

    :return: the updated pool record

    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    """
    pool = PoolService.get_pool_by_id(db=db, id=pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found!")
    return PoolService.patch_pool(db=db, id=pool_id, pool_data=pool_data)


@router.delete("/{pool_id}")
def delete_pool(pool_id: str, db: Session = Depends(get_db)):
    """
    Deletes the pool with the given ID.

    :param pool_id: pool ID
    :param db: Database session

    :return: a json with a "detail" key indicating success
    """
    if not PoolService.get_pool_by_id(db=db, id=pool_id):
        raise HTTPException(status_code=404, detail="Pool not found!")
    return PoolService.delete_pool(db=db, id=pool_id)
