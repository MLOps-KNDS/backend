import pytest
import sqlalchemy
from unittest.mock import patch
from auth.jwt_bearer import JWTBearer
from fastapi.testclient import TestClient

import models
from main import app
from services import get_db
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


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    def mock_authenticate():
        with patch.object(JWTBearer, "__call__") as mock_call:
            # Implement the desired behavior of the mocked __call__ method
            mock_call.return_value = "mocked_token"

            yield

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[JWTBearer] = mock_authenticate
    yield TestClient(app)
    del app.dependency_overrides[get_db]
    del app.dependency_overrides[JWTBearer]
