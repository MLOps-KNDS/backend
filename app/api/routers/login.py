import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

# from sqlalchemy.orm import Session # TODO: Uncomment this line when using database


from config.config import settings


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


async def get_current_user(request: Request):
    if request.session.get("user"):
        return request.session["user"]
    raise HTTPException(401, "Unauthorized")


@router.get("/me")
async def me(user=Depends(get_current_user)):
    return user


@router.get("/auth")
async def auth(request: Request):
    _logger.info("Authenticating user")
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    if user:
        _logger.info(f"User {user} authenticated")
        bearer_token = token.get("id_token")
        user.update({"token": bearer_token})
        request.session["user"] = dict(user)
    return RedirectResponse(url="/me")


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    _logger.info(f"Redirect URI: {redirect_uri}")
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
