import pytest
import sqlalchemy
from .config.config import settings
import models

engine = sqlalchemy.create_engine(
    settings.TEST_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True
)


@pytest.fixture(scope="session", autouse=True)
def setup():
    # Set up the database
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield
    # Teardown the database
    models.Base.metadata.drop_all(bind=engine)
