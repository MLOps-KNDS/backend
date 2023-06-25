"""
This module contains the API routes and their corresponding
functions for handling mlflow-server-related requests.
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import mlflow_server as mlflow_server_schemas
from services import get_db, MlflowServerService
from auth.jwt_bearer import JWTBearer


router = APIRouter(
    prefix="/mlflow-server", tags=["mlflow-server"], dependencies=[Depends(JWTBearer)]
)


@router.get(
    "/{mlflow_server_id}",
    response_model=mlflow_server_schemas.MlflowServer,
    status_code=200,
)
async def get_mlflow_server(mlflow_server_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific mlflow server by ID.

    :param mlflow_server_id: the mlflow server ID to retrieve
    :param db: Database session

    :raise HTTPException: 404 status code with "Mlflow server not found!" message
    if the specified gate ID does not exist in the database.

    :return: the mlflow server data corresponding to the given ID
    """
    mlflow_server = MlflowServerService.get_mlflow_server_by_id(
        db=db, id=mlflow_server_id
    )
    if not mlflow_server:
        raise HTTPException(status_code=404, detail="Mlflow server not found!")
    return mlflow_server


@router.get(
    "/", response_model=list[mlflow_server_schemas.MlflowServer], status_code=200
)
async def get_mlflow_servers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieves a list of mlflow server with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :raise HTTPException: 404 status code with "Mlflow server not found!" message
    if the specified range of gate ID's does not exist in the database.

    :return: a list of mlflow server data, where skip < mlflow_server_id < limit
    """
    mlflow_servers = MlflowServerService.get_mlflow_servers(
        skip=skip, limit=limit, db=db
    )
    return mlflow_servers


@router.put("/", response_model=mlflow_server_schemas.MlflowServer, status_code=201)
async def put_mlflow_server(
    mlflow_server_data: mlflow_server_schemas.MlflowServerPut,
    db: Session = Depends(get_db),
):
    """
    Creates a new mlflow server with the given information
    and returns the mlflow server information.

    :param mlflow_server_data: the information of the new mlflow server to be created.
    :param db: Database session

    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name for mlflow server already exists in the database

    :return: the newly-inserted mlflow server record
    """
    if MlflowServerService.get_mlflow_server_by_name(
        db=db, name=mlflow_server_data.name
    ):
        raise HTTPException(status_code=409, detail="Name already registered")
    return MlflowServerService.put_mlflow_server(
        db=db, mlflow_server_data=mlflow_server_data
    )


@router.patch(
    "/{mlflow_server_id}",
    response_model=mlflow_server_schemas.MlflowServer,
    status_code=200,
)
async def patch_mlflow_server(
    mlflow_server_id: int,
    mlflow_server_data: mlflow_server_schemas.MlflowServerPatch,
    db: Session = Depends(get_db),
):
    """
    Updates the information of an existing mlflow server with the provided data and
    returns the updated mlflow server information.

    :param mlflow_server_id: the mlflow server ID to patch
    :param mlflow_server_data: the information of the new mlflow server to be created.
    :param db: Database session

    :raise HTTPException: 404 status code with "Mlflow server not found!" message
    if the specified mlflow server ID does not exist in the database.
    :raise HTTPException: 409 status code with "Name already registered"
    message if the provided name for mlflow server already exists in the database

    :return: the updated mlflow server record
    """
    gate = MlflowServerService.get_mlflow_server_by_id(db=db, id=mlflow_server_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Mlflow server not found!")
    if MlflowServerService.get_mlflow_server_by_name(
        db=db, name=mlflow_server_data.name
    ):
        raise HTTPException(status_code=409, detail="Name already registered")
    return MlflowServerService.patch_mlflow_server(
        db=db, mlflow_server_id=mlflow_server_id, mlflow_server_data=mlflow_server_data
    )


@router.delete("/{mlflow_server_id}", status_code=200)
async def delete_mlflow_server(mlflow_server_id: int, db: Session = Depends(get_db)):
    """
    Deletes the mlflow server with the specified email.

    :param id: The id of the mlflow server to be deleted.
    :param db: Database session

    :raise HTTPException: 404 status code with "Mlflow server not found!" message
    if the specified mlflow server ID does not exist in the database.

    :return: the updated mlflow server record
    """
    if not MlflowServerService.get_mlflow_server_by_id(db=db, id=mlflow_server_id):
        raise HTTPException(status_code=404, detail="Mlflow server not found!")
    return MlflowServerService.delete_mlflow_server(db=db, id=mlflow_server_id)
