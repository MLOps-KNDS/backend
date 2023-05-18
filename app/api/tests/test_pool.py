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
    test_pool = pool_schemas.PutPool(
        name="test_name",
        description="test_description",
        created_by=user_id,
    )

    response = client.put(POOL_ROUTE, json=dict(test_pool))

    assert response.status_code == 201, response.text
    assert "id" in response.json()