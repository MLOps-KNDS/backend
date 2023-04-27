"""
This module provides services which are used
to send requests directly to the database
"""

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from schemas import gate as gate_schemas
from models import gate as gate_models
from datetime import datetime


class GateService:
    @classmethod
    def get_gate_by_id(cls, db: Session, id: int) -> gate_models.Gate | None:
        """
        Returns the gate data found by gate id

        :param db: Database session
        :param id: the gate ID to retrieve

        :return: the gate data corresponding to the given ID or None if not found
        """
        return db.query(gate_models.Gate).filter(gate_models.Gate.id == id).first()

    @classmethod
    def get_gate_by_name(cls, db: Session, name: str) -> gate_models.Gate | None:
        """
        Returns the gate data found by gate name

        :param db: Database session
        :param name: the gate name to retrieve

        :return: the gate data corresponding to the given name or None if not found
        """
        return db.query(gate_models.Gate).filter(gate_models.Gate.name == name).first()

    @classmethod
    def get_gates(
        cls, db: Session, skip: int = 0, limit: int = 100
    ) -> list[gate_models.Gate] | None:
        """
        Returns a list of gate data, with optional pagination

        :param db: Database session
        :param skip: (optional) the number of records to skip (default: 0)
        :param limit: (optional) the maximum number of records to retrieve
        (default: 100)

        :return: a list of gate data, where skip < gate_id < limit
        """

        return db.query(gate_models.Gate).offset(skip).limit(limit).all()

    @classmethod
    def put_gate(cls, db: Session, gate_data: gate_schemas.GatePut) -> gate_models.Gate:
        """
        Inserts a new gate record into the database

        :param db: Database session
        :param gate_data: the gate data to insert

        :return: the newly-inserted gate record
        """
        db_gate = gate_models.Gate(**gate_data.dict())
        creation_time = datetime.utcnow()
        db_gate.updated_by = db_gate.created_by
        db_gate.created_at = creation_time
        db_gate.updated_at = creation_time
        db.add(db_gate)
        db.commit()
        db.refresh(db_gate)
        return db_gate

    @classmethod
    def patch_gate(
        cls, db: Session, gate_id: int, gate_data: gate_schemas.GatePatch
    ) -> gate_models.Gate:
        """
        Updates an existing gate record in the database

        :param db: Database session
        :param gate_id: the gate ID to patch
        :param gate_data: the gate data to update

        :return: the updated gate record
        """
        db_gate = GateService.get_gate_by_id(db=db, id=gate_id)
        for key, value in gate_data.dict(exclude_none=True).items():
            setattr(db_gate, key, value)
        db.add(db_gate)
        db.commit()
        db.refresh(db_gate)
        return db_gate

    @classmethod
    def delete_gate(cls, db: Session, id: str) -> JSONResponse:
        """
        Deletes a gate record from the database

        :param db: Database sessioner
        :param id: the gate ID to delete

        :return: a json with a "detail" key indicating success
        """
        db.query(gate_models.Gate).filter(gate_models.Gate.id == id).delete()
        db.commit()
        return JSONResponse({"detail": "success"}, status_code=200)
