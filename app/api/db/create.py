"""
This module creates a database if not already exists.

This main() function from this method should be called
with each start of the program.
"""

import models.base
from db.session import engine
from sqlalchemy import Engine
import logging

_logger = logging.getLogger(__name__)


def create_db(engine: Engine) -> dict:
    """Creates all tables from ORM models

    :param db: Database session
    :return: A dict with the status and an optional message
    """
    _logger.info("Creating database from ORM models...")
    try:
        models.base.Base.metadata.create_all(bind=engine)
    except Exception as e:
        _logger.error(f"Creating database from ORM models failed with error {e}")
        raise e
    else:
        _logger.info("Creating database from ORM models finished")
        return {"status": "ok"}


def main() -> None:
    """
    Function calls creation of database
    """
    create_db(engine)


if __name__ == "__main__":
    main()
