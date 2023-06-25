import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from unittest.mock import patch
import importlib

import models
from auth.jwt_bearer import JWTBearer
from main import app
from services import get_db
from .db.session import engine
import auth.jwt_handler

@pytest.fixture(scope="session", autouse=True)
def setup():
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("CREATE SCHEMA IF NOT EXISTS core"))
        conn.commit()

    # Set up the database
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                "INSERT INTO core.user (name, surname, email) "
                "VALUES ('test_name', 'test_surname', 'test@test.com')"
            )
        )
        conn.commit()
    yield
    # Teardown the database
    models.Base.metadata.drop_all(bind=engine)

    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("DROP SCHEMA IF EXISTS core"))
        conn.commit()

@pytest.fixture(autouse=True)
def override_decode_jwt_token(monkeypatch):
    def custom_decode_jwt_token(token):
        return {"user_id": int(token)}

    monkeypatch.setattr(auth.jwt_handler, "decode_jwt_token", custom_decode_jwt_token)
    
@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    class CustomJWTBearer(JWTBearer):
        def __call__(self, request):
            credentials = request.headers.get("Authorization")
            token = credentials.split(" ")[1]
            return token
        def verify_jwt(self, jwtoken: str) -> bool:
            return True

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[JWTBearer] = CustomJWTBearer()
    yield TestClient(app)
    del app.dependency_overrides[get_db]
    del app.dependency_overrides[JWTBearer]
