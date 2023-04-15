from sqlalchemy import create_engine, Connection, text
import os
from typing import Optional
from db_config import config_env, config_ini


def get_url(config: dict) -> str:
    """Generates the url for connection

    ...
    :param config: Database connection config
    :type config: dict
    ...
    :return: Database connection url
    :rtype: str
    """

    return "postgresql://{}:{}@{}:{}/{}".format(
        config["user"],
        config["password"],
        config["host"],
        config["port"],
        config["dbname"],
    )


def connect(config: Optional[dict] = None) -> Connection:
    """Connects to the database

    ...
    :param config: Database connection config, defaults to None
    :type config: Optional[dict], optional
    ...
    :return: Database connection
    :rtype: Connection
    """
    # Check if config was passed
    if config is not None:
        conn = create_engine(get_url(config)).connect()
        if conn:
            return conn
        else:
            raise Exception("Connection failed, check your credentials")

    # Check if environment variables are set
    env_vars_found = True
    env_vars = [
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_NAME",
        "POSTGRES_USER",
        "POSTGRES_PASS",
    ]
    for var in env_vars:
        if os.environ.get(var) is None:
            print(f"Enviroment var {var} not set, looking for database.ini")
            env_vars_found = False
            break
    if env_vars_found:
        config = config_env()
    else:
        config = config_ini()

    conn = create_engine(get_url(config)).connect()
    if conn:
        return conn
    else:
        raise Exception("Connection failed, check your credentials")


if __name__ == "__main__":
    conn = connect()

    # get postgresql version
    record = conn.execute(text("SELECT version();")).fetchone()
    # record = cursor.fetchone()
    print(f"Connected to {record}")

    # close the connection
    conn.close()
