"""
This module provides services which are used
to send requests directly to the database
"""

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime

from schemas import mlflow_server as mlflow_server_schemas
from models import mlflow_server as mlflow_server_models


class MlflowServerService:
    @classmethod
    def get_mlflow_server_by_id(
        cls, db: Session, id: int
    ) -> mlflow_server_models.MlflowServer | None:
        """
        Returns the mlflow server data found by gate id

        :param db: Database session
        :param id: the mlflow server ID to retrieve

        :return: the mlflow server data corresponding to the given ID
        or None if not found
        """
        return (
            db.query(mlflow_server_models.MlflowServer)
            .filter(mlflow_server_models.MlflowServer.id == id)
            .first()
        )

    @classmethod
    def get_mlflow_server_by_name(
        cls, db: Session, name: str
    ) -> mlflow_server_models.MlflowServer | None:
        """
        Returns the mlflow server data found by gate name

        :param db: Database session
        :param name: the mlflow server name to retrieve

        :return: the mlflow server data corresponding to the given name
        or None if not found
        """
        return (
            db.query(mlflow_server_models.MlflowServer)
            .filter(mlflow_server_models.MlflowServer.name == name)
            .first()
        )

    @classmethod
    def get_mlflow_servers(
        cls, db: Session, skip: int = 0, limit: int = 100
    ) -> list[mlflow_server_models.MlflowServer]:
        """
        Returns a list of mlflow server data, with optional pagination

        :param db: Database session
        :param skip: (optional) the number of records to skip (default: 0)
        :param limit: (optional) the maximum number of records to retrieve
        (default: 100)

        :return: a list of mlflow server data, where skip < mlflow_server_id < limit
        """
        models = (
            db.query(mlflow_server_models.MlflowServer).offset(skip).limit(limit).all()
        )
        return models

    @classmethod
    def put_mlflow_server(
        cls, db: Session, mlflow_server_data: mlflow_server_schemas.MlflowServerPut
    ) -> mlflow_server_models.MlflowServer:
        """
        Inserts a new mlflow server record into the database

        :param db: Database session
        :param mlflow_server_data: the mlflow server data to insert

        :return: the newly-inserted mlflow server record
        """
        db_gate = mlflow_server_models.MlflowServer(**mlflow_server_data.dict())
        creation_time = datetime.utcnow()
        db_gate.updated_by = db_gate.created_by
        db_gate.created_at = creation_time
        db_gate.updated_at = creation_time
        db.add(db_gate)
        db.commit()
        db.refresh(db_gate)
        return db_gate

    @classmethod
    def patch_mlflow_server(
        cls,
        db: Session,
        mlflow_server_id: int,
        mlflow_server_data: mlflow_server_schemas.MlflowServerPatch,
    ) -> mlflow_server_models.MlflowServer:
        """
        Updates an existing mlflow server record in the database

        :param db: Database session
        :param mlflow_server_id: the mlflow server ID to patch
        :param mlflow_server_data: the mlflow server data to update

        :return: the updated mlflow server record
        """
        db_mlflow_server = MlflowServerService.get_mlflow_server_by_id(
            db=db, id=mlflow_server_id
        )
        for key, value in mlflow_server_data.dict(exclude_none=True).items():
            setattr(db_mlflow_server, key, value)
        db_mlflow_server.updated_at = datetime.utcnow()
        db.add(db_mlflow_server)
        db.commit()
        db.refresh(db_mlflow_server)
        return db_mlflow_server

    @classmethod
    def delete_mlflow_server(cls, db: Session, id: str) -> JSONResponse:
        """
        Deletes a mlflow server record from the database

        :param db: Database sessioner
        :param id: the mlflow server ID to delete

        :return: a json with a "detail" key indicating success
        """
        db.query(mlflow_server_models.MlflowServer).filter(
            mlflow_server_models.MlflowServer.id == id
        ).delete()
        db.commit()
        return JSONResponse({"detail": "Mlflow server deleted successfully!"})
