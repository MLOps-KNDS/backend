import pytest
import sqlalchemy
import models
from .db.session import engine


@pytest.fixture(scope="session", autouse=True)
def setup():
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("CREATE SCHEMA IF NOT EXISTS core"))
        conn.commit()

    # Set up the database
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield
    # Teardown the database
    models.Base.metadata.drop_all(bind=engine)

    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("DROP SCHEMA IF EXISTS core"))
        conn.commit()
