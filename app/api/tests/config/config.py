"""
This code defines a Pydantic BaseSettings subclass called Settings
that holds configuration values for a PostgreSQL local database.

The TEST_SQLALCHEMY_DATABASE_URI must be a URL to the valid local
PostGreSQL database on which all of the tests will be simulated.

To run tests you have to install "pytest" and run by a command: 'pytest'

See more: https://fastapi.tiangolo.com/advanced/testing-database/
"""

from pydantic import BaseSettings, validator, PostgresDsn
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_NAME: str = "test"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    TEST_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("TEST_SQLALCHEMY_DATABASE_URI", pre=True, allow_reuse=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=values.get("POSTGRES_NAME"),
        )

    class Config:
        validate_assignment = True
        check_fields = False


settings = Settings()
