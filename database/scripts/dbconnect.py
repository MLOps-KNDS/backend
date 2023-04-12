import psycopg2
import os
from typing import Optional
from dbconfig import config_env, config_ini


def connect(config: Optional[dict] = None) -> psycopg2.extensions.connection:
    """Connects to the database

    ...
    :param config: Database connection config, defaults to None
    :type config: Optional[dict], optional
    ...
    :return: Database connection
    :rtype: psycopg2.extensions.connection
    """
    # Check if config was passed
    if config is not None:
        conn = psycopg2.connect(**config)
        if conn:
            return conn
        else:
            raise Exception("Connection failed, check your credentials")

    # Check if environment variables are set
    env_vars_found = True
    env_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASS"]
    for var in env_vars:
        if os.environ.get(var) is None:
            print(f"Enviroment var {var} not set, looking for database.ini")
            env_vars_found = False
            break
    if env_vars_found:
        config = config_env()
    else:
        config = config_ini()

    conn = psycopg2.connect(**config)
    if conn:
        return conn
    else:
        raise Exception("Connection failed, check your credentials")


if __name__ == "__main__":
    conn = connect()

    # get postgresql version
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"Connected to {record}")

    # close the connection
    cursor.close()
    conn.close()
