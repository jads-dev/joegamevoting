import os

from datetime import datetime, timedelta
from typing import Optional

import requests

from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from requests_oauthlib import OAuth2Session
from starlette.responses import RedirectResponse

from app.models.auth import TokenData, User, get_user, register_user, set_can_vote
from app.discordbot import can_vote


router = APIRouter()

OAUTH2_CLIENT_ID = "687854633443655814"
OAUTH2_CLIENT_SECRET = "***REMOVED***"
OAUTH2_REDIRECT_URI = "https://joegames.nodja.com/discord_callback"

API_BASE_URL = "https://discordapp.com/api"
AUTHORIZATION_BASE_URL = API_BASE_URL + "/oauth2/authorize"
TOKEN_URL = API_BASE_URL + "/oauth2/token"

SECRET_KEY = "***REMOVED***"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 525600  # 1 year

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_userid(token: str = Depends(oauth2_scheme)):
    if not token:
        return None

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("sub")
    return user_id


async def get_optional_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return None

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("sub")
    token_data = TokenData(user_id=user_id)

    user = get_user(user_id=token_data.user_id)
    return user


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            "client_id": OAUTH2_CLIENT_ID,
            "client_secret": OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
    )


@router.get("/login")
async def login():
    scope = ["identify"]
    discord = make_session(scope=scope)
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    return RedirectResponse(url=authorization_url)


@router.get("/discord_callback")
async def discord_callback(request: Request, state: str, code: str):
    discord = make_session(state=state)
    url = str(request.url)
    url = url.replace(":8000", ":3000")
    url = url.replace("/api/", "/")
    token = discord.fetch_token(TOKEN_URL, client_secret=OAUTH2_CLIENT_SECRET, authorization_response=url)

    headers = {"Authorization": f"Bearer {token['access_token']}"}
    res = requests.get("https://discordapp.com/api/users/@me", headers=headers)

    user_data = res.json()
    user_db = get_user(user_id=user_data["id"])
    if not user_db:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}"
        register_user(user_id=user_data["id"], username=user_data["username"], avatar_url=avatar_url)
        user_db = get_user(user_id=user_data["id"])

    if not user_db["can_vote"] and await can_vote(user_db["user_id"]):
        set_can_vote(user_db["user_id"])

    access_token = create_access_token(data={"sub": str(user_db["user_id"])}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/me")
async def me(current_user: User = Depends(get_optional_current_user)):
    return current_user


@router.get("/can_vote")
async def _can_vote(current_user: User = Depends(get_optional_current_user)):
    return await can_vote(current_user["user_id"])
