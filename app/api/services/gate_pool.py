from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from schemas.pool import Pool
from models import gate as gate_models


class GatePoolService:
    """
    Contains methods for interacting with the pool_model table.
    """

    @classmethod
    def get_pools(cls, db: Session, gate_id: int, skip: int, limit: int) -> list[Pool]:
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
            db.query(gate_models.GatePool)
            .filter(gate_models.GatePool.gate_id == gate_id)
            .order_by(gate_models.GatePool.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        pools = [record.pool for record in gate_pools]
        return pools

    @classmethod
    def put_pool_gate(cls, db: Session, gate_id: int, pool_id: int) -> JSONResponse:
        """
        Inserts a new gate pool record into the database

        :param db: Database session
        :param gate_id: the gate ID to retrieve
        :param pool_data: the pool data to insert

        :return: JSONResponse with a "detail" key indicating success
        """
        db_gate_pool = gate_models.GatePool(pool_id=pool_id, gate_id=gate_id)
        db.add(db_gate_pool)
        db.commit()
        db.refresh(db_gate_pool)
        return JSONResponse(status_code=201, content={"detail": "success"})

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
        db.query(gate_models.GatePool).filter(
            gate_models.GatePool.gate_id == gate_id,
            gate_models.GatePool.pool_id == pool_id,
        ).delete()
        db.commit()
        return JSONResponse(
            status_code=200, content={"detail": "Pool deleted successfully!"}
        )

    @classmethod
    def get_pool_by_id(
        cls, db: Session, gate_id: int, pool_id: int
    ) -> gate_models.GatePool | None:
        """
        Returns the gate pool data found by gate id and pool id

        :param db: Database session
        :param gate_id: the gate ID to retrieve
        :param pool_id: the pool ID to retrieve

        :return: the gate pool data corresponding to the given ID or None if not found
        """
        return (
            db.query(gate_models.GatePool)
            .filter(
                gate_models.GatePool.gate_id == gate_id,
                gate_models.GatePool.pool_id == pool_id,
            )
            .first()
        )
