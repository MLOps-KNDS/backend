"""
Integration module for the user endpoints.

For each of the endpoints, given function makes a request to the API
using the "client", validates that the response and the expected output.

Note that this function requires a database session to be created prior to
running. The session can be created by running the `create_test_session`
function from the `test_db.session` module.

This test file covers the following endpoints:
- PUT /user/: creates a new user with the given information.
- PATCH /user/{user_id}: updates an existing user with the given information.
- GET /user/{user_id}: retrieves an existing user with the given ID.
- GET /user/: retrieves a list of all existing users.
- DELETE /user/{user_id}: deletes an existing user with the given ID.

This function assumes that the Database is running and accessible at the URL,
set on the test_config.config.settings.
"""

import schemas.user as user_schemas
from .db.session import client, session


ROUTE = "/user/"


def test_user_put(client):
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(ROUTE, json=dict(test_user))
    assert response.status_code == 200
    assert "id" in response.json()


def test_user_patch(client):
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(ROUTE, json=dict(test_user))
    assert response.status_code == 200
    user_id = response.json()["id"]

    test_user_patch = user_schemas.UserPatch(
        name="test_patch_name",
        surname="test_patch_surname",
        email="test_patch_email@abc.com",
    )
    response = client.patch(f"{ROUTE}{user_id}", json=dict(test_user_patch))
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "id": user_id,
        "name": "test_patch_name",
        "surname": "test_patch_surname",
        "email": "test_patch_email@abc.com",
    }


def test_user_get(client):
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(ROUTE, json=dict(test_user))
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.get(f"{ROUTE}{user_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": user_id,
        "name": "test_name",
        "surname": "test_surname",
        "email": "test_email@abc.com",
    }


def test_users_get(client):
    test_user_1 = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email_1@abc.com"
    )
    response_user_1 = client.put(ROUTE, json=dict(test_user_1))
    assert response_user_1.status_code == 200

    test_user_2 = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email_2@abc.com"
    )
    response_user_2 = client.put(ROUTE, json=dict(test_user_2))
    assert response_user_2.status_code == 200

    params = {"skip": 0, "limit": 3}
    response = client.get(ROUTE, params=params)
    assert response.status_code == 200
    data = response.json()
    assert data == [response_user_1.json(), response_user_2.json()]


def test_user_delete(client):
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(ROUTE, json=dict(test_user))
    assert response.status_code == 200
    user_id = response.json()["id"]

    del_response = client.delete(f"{ROUTE}{user_id}")
    assert del_response.status_code == 200
    assert del_response.json() == {"detail": "success"}
