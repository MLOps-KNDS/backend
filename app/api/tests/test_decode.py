from auth.jwt_handler import decode_jwt_token

def test_decode_jwt_token():
    token = "123456"
    result = decode_jwt_token(token)
    assert result == {"user_id": 123456}
