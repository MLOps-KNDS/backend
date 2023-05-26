import schemas.user as user_schemas
import schemas.test as test_schemas

from .db.session import client, session

USER_ROUTE = "/user"
TEST_ROUTE = "/test"

def create_user(client, email) -> int:
    # Create user first
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email=email
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    return response.json()["id"]

def test_test_put(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a test
    test_test = test_schemas.TestPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(TEST_ROUTE, json=dict(test_test))
    
    assert response.status_code == 201, response.text
    assert "id" in response.json()

    response = client.put(TEST_ROUTE, json=dict(test_test))

    assert response.status_code == 409, response.text
    assert response.json()["detail"] == "Name already registered"

def test_test_get(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a test
    test_test = test_schemas.TestPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(TEST_ROUTE, json=dict(test_test))
    test_id = response.json()["id"]
    expected_response = response.json()

    response = client.get(f"{TEST_ROUTE}/{test_id}")
    assert response.status_code == 200, response.text
    assert response.json() == expected_response

    response = client.get(f"{TEST_ROUTE}/{test_id+1}")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Test not found!"

def test_test_delete(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a test
    test_test = test_schemas.TestPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(TEST_ROUTE, json=dict(test_test))
    test_id = response.json()["id"]

    response = client.delete(f"{TEST_ROUTE}/{test_id}")
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "success"

    response = client.delete(f"{TEST_ROUTE}/{test_id}")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Test not found!"

def test_test_patch(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a test
    test_test = test_schemas.TestPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(TEST_ROUTE, json=dict(test_test))
    test_id = response.json()["id"]

    test_patch = test_schemas.TestPatch(
        name="test_name_patch",
        description="test_description_patch",
        updated_by=user_id,
    )

    response = client.patch(f"{TEST_ROUTE}/{test_id}", json=dict(test_patch))
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "test_name_patch"
    assert response.json()["description"] == "test_description_patch"

    response = client.patch(f"{TEST_ROUTE}/{test_id+1}", json=dict(test_patch))
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Test not found!"

def test_tests_get(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a test
    test_test = test_schemas.TestPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    

