"""
This module contains the API routes and their corresponding
functions for handling gate-model-related requests.
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.pool import Pool
from services import get_db, GateService, PoolService


router = APIRouter(prefix="/{gate_id}/pool", tags=["gate-pool"])


@router.get("/", response_model=list[Pool], status_code=200)
async def get_pools(
    gate_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieves a list of gates with pagination options (skip, limit).

    :param gate_id: the gate ID to retrieve
    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :raise HTTPException: 404 status code with "Pools not found!" message
    if gate has no pools.

    :return: a list of gate pools data, where skip < number of pools < limit
    """
    if not GateService.get_gate_by_id(db=db, id=gate_id):
        raise HTTPException(status_code=404, detail="Gate not found!")
    pools = GateService.get_pools(db=db, gate_id=gate_id, skip=skip, limit=limit)
    return pools


@router.put("/{pool_id}", status_code=201)
async def put_pool_gate(
    gate_id: int,
    pool_id: int,
    db: Session = Depends(get_db),
):
    """
    Adds existing pool to gate.

    :param gate_id: the gate ID to retrieve
    :param pool_id: the pool ID to retrieve
    :param db: Database session

    :raise HTTPException: 404 status code with "Gate not found!" message
    if the specified gate ID does not exist in the database.
    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.
    :raise HTTPException: 409 status code with "Pool already in gate!"
    message if the specified pool ID already in gate.

    :return: JSON response with status code 201
    """

    if not GateService.get_gate_by_id(db=db, id=gate_id):
        raise HTTPException(status_code=404, detail="Gate not found!")
    if not PoolService.get_pool_by_id(db=db, id=pool_id):
        raise HTTPException(status_code=404, detail="Pool not found!")
    if GateService.get_pool_by_id(db=db, gate_id=gate_id, pool_id=pool_id):
        raise HTTPException(status_code=409, detail="Pool already in gate!")

    return GateService.put_pool_gate(db=db, gate_id=gate_id, pool_id=pool_id)


@router.delete("/{pool_id}", status_code=200)
async def delete_pool_gate(gate_id: int, pool_id: int, db: Session = Depends(get_db)):
    """
    Deletes pool from gate.

    :param gate_id: The id of the gate from which to delet.
    :param pool_id: The id of the pool to be deleted.
    :param db: Database session

    :raise HTTPException: 404 status code with "Gate not found!" message
    if the specified gate ID does not exist in the database.
    :raise HTTPException: 404 status code with "Pool not found!" message
    if the specified pool ID does not exist in the database.

    :return: JSON response with status code 200
    """
    if not GateService.get_gate_by_id(db=db, id=gate_id):
        raise HTTPException(status_code=404, detail="Gate not found!")
    if not PoolService.get_pool_by_id(db=db, id=pool_id):
        raise HTTPException(status_code=404, detail="Pool not found!")
    if not GateService.get_pool_by_id(db=db, gate_id=gate_id, pool_id=pool_id):
        raise HTTPException(status_code=404, detail="Pool is not in gate!")

    return GateService.delete_pool_gate(db=db, gate_id=gate_id, pool_id=pool_id)
