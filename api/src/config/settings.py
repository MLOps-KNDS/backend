from pydantic import BaseSettings

#  we can add different settings for every module
#  in addition we can add .env file


class DatabaseSettings(BaseSettings):
    host: str = "localhost"
    port: str = "5432"
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"


database_settings = DatabaseSettings()
