"""
This module creates a database if not already exists.

This main() function from this method should be called
with each start of the program.
"""

import logging
from sqlalchemy import text
from .session import engine, SessionLocal


import models
from services import UserService
from services import MlflowServerService
from schemas import user as user_schemas
from schemas import mlflow_server as mlflow_server_schemas

_logger = logging.getLogger(__name__)


def create_db() -> dict:
    """Creates all tables from ORM models

    :param db: Database session
    :return: A dict with the status and an optional message
    """
    _logger.info("Creating database from ORM models...")
    try:
        # Create schema core
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS core"))
            conn.commit()

        # Create all tables
        models.Base.metadata.create_all(bind=engine, checkfirst=True)
        _logger.info(f"List of all tables: {models.Base.metadata.tables.keys()}")
    except Exception as e:
        _logger.error(f"Creating database from ORM models failed with error {e}")
        raise e
    else:
        _logger.info("Creating database from ORM models finished")

    # Insert initial data
    _logger.info("Inserting initial data...")
    try:
        db = SessionLocal()
        # Super user
        user = user_schemas.UserPut(
            name="SYSTEM",
            surname="SYSTEM",
            email="system@system.com",
        )
        db_user = UserService.put_user(db, user)
        _logger.info("Created system user")
        # System mlflow server
        mlflow_server = mlflow_server_schemas.MlflowServerPut(
            name="SYSTEM",
            tracking_uri="http://tyro-mlflow:80",
        )
        MlflowServerService.put_mlflow_server(db, mlflow_server, db_user.id)
        _logger.info("Created system mlflow server")

    except Exception as e:
        _logger.error(f"Inserting initial data failed with error {e}")
        raise e
    finally:
        db.close()

    return {"status": "ok"}
