from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.settings import database_settings


def get_url() -> str:
    """
    Generates the url for connection

    :return: Database connection url
    """

    return "postgresql://{}:{}@{}:{}/{}".format(
        database_settings.user,
        database_settings.password,
        database_settings.host,
        database_settings.port,
        database_settings.name,
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
