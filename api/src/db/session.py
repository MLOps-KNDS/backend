from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from db_config import config_env, config_ini


def get_url() -> str:
    """
    Generates the url for connection

    :return: Database connection url
    """

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

    return "postgresql://{}:{}@{}:{}/{}".format(
        config["user"],
        config["password"],
        config["host"],
        config["port"],
        config["dbname"],
    )


engine = create_engine(get_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    conn = create_engine(get_url(), pool_pre_ping=True).connect()

    # get postgresql version
    record = conn.execute(text("SELECT version();")).fetchone()
    # record = cursor.fetchone()
    print(f"Connected to {record}")

    # close the connection
    conn.close()
