from src.models.base_class import Base
from sqlalchemy import create_engine
from .session import get_url
from sqlalchemy.engine import Engine
import logging

_logger = logging.getLogger(__name__)


async def create_db(engine: Engine) -> dict:
    """Creates all tables from ORM models

    ...
    :param engine: Database connection
    ...
    :return: A dict with the status and an optional message
    """
    _logger.info("Creating database from ORM models...")
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        _logger.error(f"Creating database from ORM models failed with error {e}")
        raise e
    else:
        _logger.info("Creating database from ORM models finished")
        return {"status": "ok"}


if __name__ == "__main__":
    import asyncio

    # print(config_ini())
    engine = create_engine(get_url(), pool_pre_ping=True)

    response = asyncio.run(create_db(engine))
    print(response)
