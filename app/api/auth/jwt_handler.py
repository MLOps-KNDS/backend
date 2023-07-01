import jwt
import logging
import time
from config.config import settings


_logger = logging.getLogger(__name__)


def token_response(token: str) -> dict:
    """
    Create a token response with the JWT token

    :param token: The JWT token
    :return: The token response
    """
    return {"access_token": token}


def create_jwt_token(user_id: int) -> dict:
    """
    Create a JWT token with the user id and expiration time

    :param user_id: The user id
    :return: The JWT token
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + settings.TOKEN_EXPIRE_SECONDS,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token_response(token)


def decode_jwt_token(token: str) -> dict:
    """
    Decode a JWT token

    :param token: The JWT token
    :return: The decoded token
    """
    try:
        decode_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decode_token if decode_token["expires"] >= time.time() else {}
    except Exception as e:
        _logger.exception(f"Error decoding token with an exception {e}")
        return {}
