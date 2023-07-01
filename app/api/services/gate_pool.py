from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from models import gate as gate_pool_models


class GatePoolService:
    """
    Contains methods for interacting with the pool_model table.
    """

    @classmethod
    def get_gate_pool_by_pool_id(
        cls, db: Session, gate_id: int, pool_id: int
    ) -> gate_pool_models.GatePool:
        """
        Returns the pool in the given gate pool data found by pool ID

        :param gate_id: the given gate pool ID to where to look for the pool ID
        :param pool_id: the pool ID to retrieve

        :return: the gate pool data corresponding to the given IDs or None if not found
        """
        return (
            db.query(gate_pool_models.GatePool)
            .filter(gate_pool_models.GatePool.gate_id == gate_id)
            .filter(gate_pool_models.GatePool.pool_id == pool_id)
            .first()
        )

    @classmethod
    def get_gate_pool_by_id(cls, db: Session, id: int) -> gate_pool_models.GatePool:
        """
        Returns the gate pool data found by ID

        :param id: the gate pool ID to retrieve

        :return: the gate pool data corresponding to the given ID or None if not found
        """
        return (
            db.query(gate_pool_models.GatePool)
            .filter(gate_pool_models.GatePool.gate_id == id)
            .first()
        )

    @classmethod
    def get_gate_pools(
        cls, db: Session, gate_id: int, skip: int, limit: int
    ) -> list[gate_pool_models.GatePool]:
        """
        Returns a list of gate pools, with optional pagination

        :param db: Database session
        :param gate_id: the gate ID to retrieve
        :param skip: (optional) the number of records to skip (default: 0)
        :param limit: (optional) the maximum number of records to retrieve
        (default: 100)

        :return: a list of gate pools, where skip < GatePool.id < limit
        """
        gate_pools = (
            db.query(gate_pool_models.GatePool)
            .filter(gate_pool_models.GatePool.gate_id == gate_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return gate_pools

    @classmethod
    def put_pool_gate(
        cls, db: Session, gate_id: int, pool_id: int
    ) -> gate_pool_models.GatePool:
        """
        Inserts a new gate pool record into the database

        :param db: Database session
        :param gate_id: the gate ID to retrieve
        :param pool_data: the pool data to insert

        :return: JSONResponse with a "detail" key indicating success
        """
        db_gate_pool = gate_pool_models.GatePool(pool_id=pool_id, gate_id=gate_id)
        db.add(db_gate_pool)
        db.commit()
        db.refresh(db_gate_pool)
        return db_gate_pool

    @classmethod
    def delete_pool_gate(
        cls,
        db: Session,
        gate_id: int,
        pool_id: int,
    ) -> JSONResponse:
        """
        Deletes a gate pool record from the database

        :param db: Database session
        :param gate_id: the gate ID to retrieve
        :param pool_id: the pool ID to retrieve

        :return: JSONResponse with a "detail" key indicating success
        """
        db.query(gate_pool_models.GatePool).filter(
            gate_pool_models.GatePool.gate_id == gate_id
        ).filter(gate_pool_models.GatePool.pool_id == pool_id).delete()
        db.commit()
        return JSONResponse(content={"detail": "success"})
