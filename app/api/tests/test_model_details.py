import schemas.model as model_schemas
import schemas.user as user_schemas
import schemas.model_details as model_details_schemas
from .db.session import client, session

USER_ROUTE = "/user"
MODEL_ROUTE = "/model"


def test_model_details_get(client):
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
    model_id = response.json()["id"]

    response = client.get(f"{MODEL_ROUTE}/{model_id}/details")

    excpected_output = {
        "model_id": model_id,
        "artifact_uri": None,
        "image_tag": None,
        "replicas": None,
        "cpu_request": None,
        "cpu_limit": None,
        "memory_request": None,
        "memory_limit": None,
    }

    assert response.status_code == 200, response.text
    assert "id" in response.json()
    for k in excpected_output.keys():
        assert response.json()[k] == excpected_output[k]
    # Test for exception
    response = client.get(f"{MODEL_ROUTE}/{model_id+1}/details")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "ModelDetails not found!"}


def test_model_details_patch(client):
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
    model_id = response.json()["id"]

    test_patch = model_details_schemas.PatchModelDetails(
        artifact_uri="test_artifact_uri",
        image_tag="test_image_tag",
        replicas=1,
        cpu_request="test_cpu_request",
        cpu_limit="test_cpu_limit",
        memory_request="test_memory_request",
        memory_limit="test_memory_limit",
    )

    response = client.patch(f"{MODEL_ROUTE}/{model_id}/details", json=dict(test_patch))

    assert response.status_code == 200, response.text
    assert "id" in response.json()
    assert response.json()["model_id"] == model_id
    for k in test_patch.dict().keys():
        assert response.json()[k] == test_patch.dict()[k]
    # Test for exception
    response = client.patch(
        f"{MODEL_ROUTE}/{model_id+1}/details", json=dict(test_patch)
    )
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "ModelDetails not found!"}

    test_model_2 = model_schemas.PutModel(
        name="test_name_2",
        description="test_description",
        status=model_schemas.Status.ACTIVE,
        created_by=user_id,
    )
    response = client.put(MODEL_ROUTE, json=dict(test_model_2))
    model_id_2 = response.json()["id"]
    response = client.patch(
        f"{MODEL_ROUTE}/{model_id_2}/details", json=dict(test_patch)
    )
    assert response.status_code == 400, response.text
    assert response.json() == {
        "detail": "ModelDetails with the same tag already exists!"
    }
