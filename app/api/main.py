"""
This is the main module.
It contains the FastAPI app.
"""

import time
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

from db.create import create_db
from db.session import engine

from routers import (
    user,
    pool,
    gate,
    model,
    test,
)


@asynccontextmanager
async def init(app: FastAPI):
    time.sleep(5)
    create_db(engine)
    yield


app = FastAPI(
    title="Backend Service",
    description="Backend Service for the ML Platform",
    version="0.1.0",
    lifespan=init,
)


class UserValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excludes: list[str] = None):
        super().__init__(app)
        if excludes is None:
            excludes = []
        self.excludes = excludes

    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path in self.excludes:
                # Skip middleware processing for excluded route
                return await call_next(request)
            if not request.session.get("user"):
                raise HTTPException(status_code=401, detail="Unauthorized")
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )


app.add_middleware(UserValidationMiddleware, excludes=["/login", "/auth", "/logout"])
app.add_middleware(SessionMiddleware, secret_key="secret-string")


config = Config("config.env")  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

app.include_router(model.router)
app.include_router(user.router)
app.include_router(pool.router)
app.include_router(gate.router)
app.include_router(test.router)


async def get_current_user(request: Request):
    if request.session.get("user"):
        return request.session["user"]
    raise HTTPException(401, "Unauthorized")


@app.get("/")
async def root() -> dict:
    """
    Root endpoint. Returns a simple message for testing purposes.
    :return: A "Hello World" message.
    """
    return {"message": "Hello World"}


@app.get("/me")
async def me(user=Depends(get_current_user)):
    return user


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
    return RedirectResponse(url="/me")


@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
