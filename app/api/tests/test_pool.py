import schemas.pool as pool_schemas
import schemas.user as user_schemas
from .db.session import client, session

USER_ROUTE = "/user"
POOL_ROUTE = "/pool"


def create_user(client, email) -> int:
    # Create user first
    test_user = user_schemas.UserPut(
        name="test_name", surname="test_surname", email=email
    )
    response = client.put(USER_ROUTE, json=dict(test_user))
    return response.json()["id"]

def test_pool_put(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a pool
    test_pool = pool_schemas.PoolPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(POOL_ROUTE, json=dict(test_pool))

    assert response.status_code == 201, response.text
    assert "id" in response.json()

    response = client.put(POOL_ROUTE, json=dict(test_pool))

    assert response.status_code == 406, response.text
    assert response.json() == {"detail": "Name already registered"}

def test_pool_patch(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a pool
    test_pool = pool_schemas.PoolPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(POOL_ROUTE, json=dict(test_pool))
    pool_id = response.json()["id"]

    test_patch_pool = pool_schemas.PoolPatch(
        name="test_patch_name",
        description="test_patch_description",
        updated_by=user_id,
    )

    response = client.patch(f"{POOL_ROUTE}/{pool_id}", json=dict(test_patch_pool))

    assert response.status_code == 200, response.text
    assert response.json()["name"] == "test_patch_name"
    assert response.json()["description"] == "test_patch_description"


    response = client.patch(f"{POOL_ROUTE}/{pool_id}", json=dict(test_patch_pool))
    assert response.status_code == 406, response.text
    



def test_pool_delete(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a pool
    test_pool = pool_schemas.PoolPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(POOL_ROUTE, json=dict(test_pool))
    pool_id = response.json()["id"]

    response = client.delete(f"{POOL_ROUTE}/{pool_id}")

    assert response.status_code == 200, response.text
    assert response.json() == {"detail": "success"}

def test_pool_get(client):
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a pool
    test_pool = pool_schemas.PoolPut(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(POOL_ROUTE, json=dict(test_pool))
    pool_id = response.json()["id"]

    response = client.get(f"{POOL_ROUTE}/{pool_id}")

    assert response.status_code == 200, response.text
    for key in test_pool.dict().keys():
        assert response.json()[key] == test_pool.dict()[key]

    response = client.get(f"{POOL_ROUTE}/{pool_id+1}")

    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Pool not found!"}

def test_pools_get(client):
    params = {"skip": 0, "limit": 3}
    # Create user first
    user_id = create_user(client, "test@test.com")

    # Now create a pool
    test_pool = pool_schemas.PoolPut(
        name="test_name_1",
        description="test_description",
        created_by=user_id,
    )
    test_pool_2 = pool_schemas.PoolPut(
        name="test_name_2",
        description="test_description",
        created_by=user_id,
    )
    test_pool_3 = pool_schemas.PoolPut(
        name="test_name_3",
        description="test_description",
        created_by=user_id,
    )

    response = client.get(POOL_ROUTE, params=params)

    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Pools not found!"}
    
    response = client.put(POOL_ROUTE, json=dict(test_pool))
    pool_id = response.json()["id"]
    response = client.put(POOL_ROUTE, json=dict(test_pool_2))
    pool_id_2 = response.json()["id"]
    response = client.put(POOL_ROUTE, json=dict(test_pool_3))
    pool_id_3 = response.json()["id"]



    response = client.get(POOL_ROUTE, params=params)

    assert response.status_code == 200, response.text
    assert len(response.json()) == 3