from pydantic import BaseSettings, validator, PostgresDsn
from typing import Optional, Dict, Any
import secrets


class Settings(BaseSettings):
    POSTGRES_HOST: str = "database"
    POSTGRES_PORT: str = "5432"
    POSTGRES_NAME: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    TOKEN_EXPIRE_SECONDS: int = 3600  # 60 * 60 = 60 minutes
    SECRET_KEY: str = secrets.token_hex(16)
    ALGORITHM: str = "HS256"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, allow_reuse=True)
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


settings = Settings()
