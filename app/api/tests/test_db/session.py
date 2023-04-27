"""
This module provides a function to create a test session with a TestClient that can be used to test FastAPI endpoints.
The test session uses a testing database created with the create_db function from the db.create module.
It also overrides the get_db dependency of the FastAPI app with a function that creates a new testing session on each call.
This allows tests to interact with the testing database in isolation from the development database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.create import create_db
from ..test_config.config import settings
from main import app
from fastapi.testclient import TestClient
from services.deps import get_db

engine = create_engine(settings.TEST_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_session() -> TestClient:
    create_db(engine=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    return client
