import schemas.gate as model_schemas
import schemas.pool as pool_schemas
import schemas.user as user_schemas
from .db.session import client, session

USER_ROUTE = "/user"
GATE_ROUTE = "/gate"
POOL_ROUTE = "/pool"

def create_user(client, email) -> int:
    # Create user first
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email=email
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    return response.json()["id"]

def test_gate_put(client):
    user_id = create_user(client, "test@test.com")

    # Now create a gate
    test_gate = model_schemas.GatePut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )
    response = client.put(GATE_ROUTE, json=dict(test_gate))

    assert response.status_code == 201, response.text
    assert "id" in response.json()


def test_gate_patch(client):
    user_id_first = create_user(client, "test@test.com")
    user_id_second = create_user(client, "test2@test.com")

    # Now create a gate
    test_gate = model_schemas.GatePut(
        name="test_name",
        description="test_description",
        created_by=user_id_first,
    )
    response = client.put(GATE_ROUTE, json=dict(test_gate))
    gate_id = response.json()["id"]

    # Now patch the gate
    test_patch_gate = model_schemas.GatePatch(
        name="test_patch_name",
        description="test_patch_description",
        updated_by=user_id_second,
    )
    response = client.patch(f"{GATE_ROUTE}/{gate_id}", json=dict(test_patch_gate))

    assert response.status_code == 200, response.text
    for key in test_patch_gate.dict().keys():
        assert response.json()[key] == test_patch_gate.dict()[key]

