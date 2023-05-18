import schemas.gate as gate_schemas
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
    test_gate = gate_schemas.GatePut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )
    response = client.put(GATE_ROUTE, json=dict(test_gate))

    assert response.status_code == 201, response.text
    assert "id" in response.json()

    response = client.put(GATE_ROUTE, json=dict(test_gate))
    assert response.status_code == 409, response.text
    assert response.json() == {"detail": "Name already registered"}


def test_gate_patch(client):
    user_id_first = create_user(client, "test@test.com")
    user_id_second = create_user(client, "test2@test.com")

    # Now create a gate
    test_gate = gate_schemas.GatePut(
        name="test_name",
        description="test_description",
        created_by=user_id_first,
    )
    response = client.put(GATE_ROUTE, json=dict(test_gate))
    gate_id = response.json()["id"]

    test_gate_patch = gate_schemas.GatePatch(
        name="test_patch_name",
        description="test_patch_description",
        updated_by=user_id_second,
    )
    response = client.patch(f"{GATE_ROUTE}/{gate_id}", json=dict(test_gate_patch))
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "test_patch_name"
    assert response.json()["description"] == "test_patch_description"
    assert response.json()["updated_by"] == user_id_second

    # Test for exceptions
    response = client.patch(f"{GATE_ROUTE}/{gate_id+1}", json=dict(test_gate_patch))
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Gate not found!"}

    response = client.patch(
        f"{GATE_ROUTE}/{gate_id}",
        json={"name": "test_patch_name", "updated_by": user_id_second},
    )
    assert response.status_code == 409, response.text
    assert response.json() == {"detail": "Name already registered"}


def test_gate_get(client):
    user_id = create_user(client, "test@test.com")

    # Now create a gate
    test_gate = gate_schemas.GatePut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(GATE_ROUTE, json=dict(test_gate))
    gate_id = response.json()["id"]

    response = client.get(f"{GATE_ROUTE}/{gate_id}")
    assert response.status_code == 200, response.text
    assert "id" in response.json()

    # Test for exceptions
    response = client.get(f"{GATE_ROUTE}/{gate_id+1}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Gate not found!"}


def test_gates_get(client):
    params = {"skip": 0, "limit": 3}
    user_id = create_user(client, "test@test.com")

    # Now create a gate
    test_gate = gate_schemas.GatePut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )
    test_gate_2 = gate_schemas.GatePut(
        name="test_name_2",
        description="test_description",
        created_by=user_id,
    )
    test_gate_3 = gate_schemas.GatePut(
        name="test_name_3",
        description="test_description",
        created_by=user_id,
    )

    response = client.get(GATE_ROUTE, params=params)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Gates not found!"

    response_1 = client.put(GATE_ROUTE, json=dict(test_gate))
    response_2 = client.put(GATE_ROUTE, json=dict(test_gate_2))
    response_3 = client.put(GATE_ROUTE, json=dict(test_gate_3))

    excpected_response = [response_1.json(), response_2.json(), response_3.json()]

    response = client.get(GATE_ROUTE, params=params)
    assert response.status_code == 200, response.text
    assert response.json() == excpected_response


def test_delete_gate(client):
    user_id = create_user(client, "test@test.com")

    # Now create a gate
    test_gate = gate_schemas.GatePut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(GATE_ROUTE, json=dict(test_gate))
    gate_id = response.json()["id"]

    response = client.delete(f"{GATE_ROUTE}/{gate_id}")
    assert response.status_code == 200, response.text
    assert response.json() == {"detail": "success"}

    # Test for exceptions
    response = client.delete(f"{GATE_ROUTE}/{gate_id}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Gate not found!"}


# def test_get_pools(client):
#     params = {"skip":0, "limit":100}
#     user_id = create_user(client, "test@test.com")

#     # Now create a gate
#     test_gate = gate_schemas.GatePut(
#         name="test_name",
#         description="test_description",
#         created_by=user_id,
#     )

#     response = client.get(POOL_ROUTE, params=params)
#     print(response.json())

#     response = client.put(GATE_ROUTE, json=dict(test_gate))
#     gate_id = response.json()["id"]

#     test_pool_1 = pool_schemas.PoolPut(
#         name="test_pool_1",
#         description="test_description",
#         created_by=user_id,
#     )
#     response_1 = client.put(f"{POOL_ROUTE}", json=dict(test_pool_1))
#     pool_id_1 = response_1.json()["id"]
#     # print(response_1.json())
#     response = client.get(f"{POOL_ROUTE}/{pool_id_1}")
#     print(response.json())

#     test_pool_2 = pool_schemas.PoolPut(
#         name="test_pool_2",
#         description="test_description",
#         created_by=user_id,
#     )
#     response_2 = client.put(f"{GATE_ROUTE}", json=dict(test_pool_2))
#     pool_id_2 = response_2.json()["id"]
#     # print(response_2.json())
#     response = client.get(f"{POOL_ROUTE}/2")
#     print(response.json())

#     test_pool_3 = pool_schemas.PoolPut(
#         name="test_pool_3",
#         description="test_description",
#         created_by=user_id,
#     )
#     response_3 = client.put(f"{GATE_ROUTE}", json=dict(test_pool_3))
#     pool_id_3 = response_3.json()["id"]
#     # print(response_3.json())
#     response = client.get(f"{POOL_ROUTE}/3")
#     print(response.json())

#     test_gate_pool_1 = gate_schemas.GatePatchAddPool(
#         pool_id=pool_id_1,
#         updated_by=user_id
#     )
#     test_gate_pool_2 = gate_schemas.GatePatchAddPool(
#         pool_id=pool_id_2,
#         updated_by=user_id
#     )
#     test_gate_pool_3 = gate_schemas.GatePatchAddPool(
#         pool_id=pool_id_3,
#         updated_by=user_id
#     )

#     response = client.put(f"{GATE_ROUTE}/{gate_id}/pool", json=dict(test_gate_pool_1))
#     response = client.put(f"{GATE_ROUTE}/{gate_id}/pool", json=dict(test_gate_pool_2))
#     response = client.get(f"{GATE_ROUTE}/{gate_id}/pool", params=params)

#     response = client.put(f"{GATE_ROUTE}/{gate_id}/pool", json=dict(test_gate_pool_3))
#     response = client.get(f"{GATE_ROUTE}/{gate_id}/pool", params=params)

#     expected_response = [response_1.json(), response_2.json(), response_3.json()]

#     assert response.status_code == 200, response.text
#     assert response.json() == expected_response
