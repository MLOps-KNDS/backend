"""
This module contains the API routes and their corresponding
functions for handling gate-related requests.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import gate as gate_schemas
from services import get_db
from services.gate import GateService


router = APIRouter(prefix="/gate", tags=["gate"])


@router.put("/", response_model=gate_schemas.Gate)
def put_gate(gate_data: gate_schemas.GatePut, db: Session = Depends(get_db)):
    """
    Creates a new gate with the given information and returns the gate information.

    :param gate_data: the information of the new gate to be created.
    :param db: Database session

    :return: the newly-inserted gate record
    """
    return GateService.put_gate(db=db, gate_data=gate_data)


@router.get("/", response_model=list[gate_schemas.Gate])
def get_gates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of gates with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :return: a list of gate data, where skip < gate_id < limit
    """
    gates = GateService.get_gates(skip=skip, limit=limit, db=db)
    return gates


@router.get("/{gate_id}", response_model=gate_schemas.Gate)
def get_gate(gate_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific gate by ID.

    :param gate_id: the gate ID to retrieve
    :param db: Database session

    :return: the gate data corresponding to the given ID

    :raise HTTPException: 404 status code with "Gate not found!" message
    if the specified gate ID does not exist in the database.
    """
    gate = GateService.get_gate_by_id(db=db, id=gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate not found!")
    return gate


@router.patch("/{gate_id}")
def patch_gate(
    gate_id: int, gate_data: gate_schemas.GatePatch, db: Session = Depends(get_db)
):
    """
    Updates the information of an existing gate with the provided data and
    returns the updated gate information.

    :param gate_id: the gate ID to patch
    :param gate_data: the information of the new gate to be created.
    :param db: Database session

    :return: the updated gate record

    :raise HTTPException: 404 status code with "Gate not found!" message
    if the specified gate ID does not exist in the database.
    """
    gate = GateService.get_gate_by_id(db=db, id=gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate not found!")
    return GateService.patch_gate(db=db, gate_id=gate_id, gate_data=gate_data)


@router.delete("/{gate_id}")
def delete_gate(gate_id: int, db: Session = Depends(get_db)):
    """
    Deletes the gate with the specified email.

    :param id: The id of the gate to be deleted.
    :param db: Database session

    :return: the updated gate record

    :raise HTTPException: 404 status code with "Gate not found!" message
    if the specified gate ID does not exist in the database.
    """
    if not GateService.get_gate_by_id(db=db, id=gate_id):
        raise HTTPException(status_code=404, detail="Gate not found!")
    return GateService.delete_gate(db=db, id=gate_id)
