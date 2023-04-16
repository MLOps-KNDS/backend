from src.models.base_class import Base
from sqlalchemy import create_engine
from session import get_url
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


"""
import os
import argparse
from configparser import ConfigParser


def config_ini(
    filename: str = os.path.join("src", "db", "database.ini"),
    section: str = "postgresql",
) -> dict:
    Reads the database.ini file and returns a dictionary
    with the database configuration

    ...
    :param filename: Name of the database.ini file
    :param section: Section of the database.ini file
    ...
    :raises Exception: Section not found in the database.ini file
    :return: Database configuration
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return db


# Get config from command line arguments
def config_env() -> dict:
    Reads the environment variables and
    returns a dictionary with the database configuration

    ...
    :return: Database configuration
    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": os.environ.get("POSTGRES_PORT", "5432"),
        "database": os.environ.get("POSTGRES_DB", "postgres"),
        "user": os.environ.get("POSTGRES_USER", "postgres"),
        "password": os.environ.get("POSTGRES_PASSWORD", "postgres"),
    }


if __name__ == "__main__":
    # Check if environment variables are set
    env_vars_found = True
    env_vars = [
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ]
    for var in env_vars:
        if os.environ.get(var) is None:
            print(f"Environment var {var} not set, looking for database.ini")
            env_vars_found = False
            break
    if env_vars_found:
        config = config_env()
    else:
        config = config_ini()
    print(config)
"""
