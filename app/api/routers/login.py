import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
from auth.jwt_handler import create_jwt_token
from sqlalchemy.orm import Session


from config.config import settings
from services.user import UserService
from services import get_db
from schemas.user import UserPut


_logger = logging.getLogger(__name__)

router = APIRouter(tags=["login"])


oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def user_login(token: dict, db: Session):
    user_email = token.get("userinfo").get("email")
    user = UserService.get_user_by_email(db, user_email)
    if not user:
        user = UserService.put_user(
            db,
            UserPut(
                name=token.get("userinfo").get("given_name"),
                surname=token.get("userinfo").get("family_name"),
                email=user_email,
            ),
        )
        _logger.info(f"User {user_email} created")
    else:
        _logger.info(f"User {user_email} already exists")

    return create_jwt_token(user.id)


@router.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    if user:
        return user_login(token, db)
    raise HTTPException(status_code=400, detail="User not authenticated")


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    _logger.info(f"Redirect URI: {redirect_uri}")
    return await oauth.google.authorize_redirect(request, str(redirect_uri))
