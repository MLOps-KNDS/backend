"""
Integration module for the user endpoints.

For each of the endpoints, this function makes a request to the API
using the TestClient, validates that the response and the expected output.

Note that this function requires a database session to be created prior to
running. The session can be created by running the `create_test_session`
function from the `test_db.session` module.
"""

import schemas.user as user_schemas
from .test_db.session import create_test_session

client = create_test_session()

ROUTE = "/user/"


def test_user():
    """
    This test function covers the following endpoints:
    - PUT /user/: creates a new user with the given information.
    - PATCH /user/{user_id}: updates an existing user with the given information.
    - GET /user/{user_id}: retrieves an existing user with the given ID.
    - GET /user/: retrieves a list of all existing users.
    - DELETE /user/{user_id}: deletes an existing user with the given ID.

    This function assumes that the API is running and accessible at the URL, 
    set on the test_config.config.settings.
    """

    # put_user
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(ROUTE, json=dict(test_user))
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    user_id = data["id"]

    # patch_user
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

    # get_user
    response = client.get(f"{ROUTE}{user_id}")
    assert response.status_code == 200
    assert response.json() == data

    # get_users
    response = client.put(ROUTE, json=dict(test_user))
    assert response.status_code == 200
    params = {"skip": 0, "limit": 100}
    response = client.get(ROUTE, params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 1

    # delete_users
    for model in data:
        del_response = client.delete(f"{ROUTE}{model['id']}")
        assert del_response.status_code == 200
        assert del_response.json() == {"detail": "success"}
