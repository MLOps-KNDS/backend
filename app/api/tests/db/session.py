"""
This module provides a function to create a test session with a TestClient
that can be used to test FastAPI endpoints.

More: https://stackoverflow.com/questions/67255653/
how-to-set-up-and-tear-down-a-database-between-tests-in-fastapi
"""

from fastapi.testclient import TestClient
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pytest

from main import app
from services.deps import get_db
from ..config.config import settings

from routers import (
    user,
    pool,
    gate,
    model,
    test,
)

engine = sqlalchemy.create_engine(
    settings.TEST_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# It creates a nested
# transaction, recreates it when the application code calls session.commit
# and rolls it back at the end.
# Based on: https://docs.sqlalchemy.org/en/14/orm/session_transaction
# .html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override as before, it uses the one provided by the
# session fixture.
@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
