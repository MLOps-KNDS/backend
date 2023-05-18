from unittest.mock import patch, Mock

import schemas.model as model_schemas
import schemas.model_details as model_details_schemas
import schemas.user as user_schemas
from .db.session import client, session
import utils


USER_ROUTE = "/user"
MODEL_ROUTE = "/model"


def test_model_put(client):
    # Create user first
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    user_id = response.json()["id"]

    # Now create a model
    test_model = model_schemas.PutModel(
        name="test_name",
        description="test_description",
        status=model_schemas.Status.ACTIVE,
        created_by=user_id,
    )
    response = client.put(MODEL_ROUTE, json=dict(test_model))

    assert response.status_code == 201, response.text
    assert "id" in response.json()

    # Test for exception
    response = client.put(MODEL_ROUTE, json=dict(test_model))
    assert response.status_code == 409, response.text
    assert response.json() == {"detail": "Name already registered"}


def test_model_patch(client):
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    user_id_first = response.json()["id"]
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email2@abc.com"
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    user_id_second = response.json()["id"]

    test_model = model_schemas.PutModel(
        name="test_name",
        description="test_description",
        status=model_schemas.Status.ACTIVE,
        created_by=user_id_first,
    )
    response = client.put(MODEL_ROUTE, json=dict(test_model))
    model_id = response.json()["id"]

    test_model_patch = model_schemas.PatchModel(
        name="test_patch_name",
        description="test_patch_description",
        status=model_schemas.Status.INACTIVE,
        updated_by=user_id_second,
    )
    expected_output = dict(test_model_patch)

    response = client.patch(f"{MODEL_ROUTE}/{model_id}", json=dict(test_model_patch))

    assert response.status_code == 200, response.text
    for k in expected_output.keys():
        assert response.json()[k] == expected_output[k]

    response = client.patch(
        f"{MODEL_ROUTE}/{model_id+1}", json={"updated_by": user_id_first}
    )
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Model not found!"}

    response = client.patch(
        f"{MODEL_ROUTE}/{model_id}",
        json={"name": "test_patch_name", "updated_by": user_id_first},
    )
    assert response.status_code == 409, response.text
    assert response.json() == {"detail": "Name already registered"}


def test_models_get(client):
    params = {"skip": 0, "limit": 3}
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    user_id = response.json()["id"]

    # Test for exception
    response = client.get(MODEL_ROUTE, params=params)
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Models not found!"}

    test_model = model_schemas.PutModel(
        name="test_name_1",
        description="test_description_1",
        status=model_schemas.Status.ACTIVE,
        created_by=user_id,
    )
    response_model_1 = client.put(MODEL_ROUTE, json=dict(test_model))

    test_model = model_schemas.PutModel(
        name="test_name_2",
        description="test_description_2",
        status=model_schemas.Status.INACTIVE,
        created_by=user_id,
    )
    response_model_2 = client.put(MODEL_ROUTE, json=dict(test_model))

    expected_response = [response_model_1.json(), response_model_2.json()]

    params = {"skip": 0, "limit": 3}
    response = client.get(MODEL_ROUTE, params=params)

    assert response.status_code == 200, response.text
    assert response.json() == expected_response


def test_model_get(client):
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    user_id = response.json()["id"]

    test_model = model_schemas.PutModel(
        name="test_name",
        description="test_description",
        status=model_schemas.Status.ACTIVE,
        created_by=user_id,
    )
    response = client.put(MODEL_ROUTE, json=dict(test_model))
    model_id = response.json()["id"]
    expected_response = response.json()
    response = client.get(f"{MODEL_ROUTE}/{model_id}")

    assert response.status_code == 200, response.text
    assert response.json() == expected_response
    # Test for exception
    response = client.get(f"{MODEL_ROUTE}/{model_id+1}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Model not found!"}


def test_model_delete(client):
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    user_id = response.json()["id"]

    test_model = model_schemas.PutModel(
        name="test_name",
        description="test_description",
        status=model_schemas.Status.ACTIVE,
        created_by=user_id,
    )
    response = client.put(MODEL_ROUTE, json=dict(test_model))
    model_id = response.json()["id"]
    response = client.delete(f"{MODEL_ROUTE}/{model_id}")

    assert response.status_code == 200
    assert response.json() == {"detail": "model deleted"}
    # Test for exceptions
    response = client.delete(f"{MODEL_ROUTE}/{model_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Model not found!"}


@patch.object(utils.model_builder.ModelBuilder, "push")
@patch.object(utils.model_builder.ModelBuilder, "build")
def test_model_build(mock_model_builder_build: Mock, mock_model_builder_push: Mock, client):
    mock_model_builder_build.return_value = None
    mock_model_builder_push.return_value = "gcr.com/423534523454325/test"

    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email="test_email@abc.com"
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    user_id = response.json()["id"]

    test_model = model_schemas.PutModel(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )
    response = client.put(MODEL_ROUTE, json=dict(test_model))
    model_id = response.json()["id"]

    test_model_details = model_details_schemas.PatchModelDetails(
        artifact_uri="/test/test/model"
    )
    response = client.patch(f"{MODEL_ROUTE}/{model_id}/details", json=dict(test_model_details))

    client.post(f"{MODEL_ROUTE}/{model_id}/build")

    model_details = client.get(f"{MODEL_ROUTE}/{model_id}/details").json()

    assert model_details["image_tag"] == "gcr.com/423534523454325/test"
    mock_model_builder_build.assert_called_once()
    mock_model_builder_push.assert_called_once()
