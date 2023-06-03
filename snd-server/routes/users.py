from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext
from typing import Literal
from pydantic import BaseModel, Field

from context import Context
from models.users import Token, UserInDB


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()


class TokenRequestPayload(BaseModel):
    username: str = Field(max_length=64, min_length=4)
    password: str = Field(max_length=64, min_length=8)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_users_router(ctx: Context) -> APIRouter:
    router = APIRouter()

    async def authenticate_user(
        username: str, password: str
    ) -> UserInDB | Literal[False]:
        user = await ctx.users_storage.get_user(username=username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    async def store_user(username: str, password: str) -> UserInDB | Literal[False]:
        user = await ctx.users_storage.store_user(username, get_password_hash(password))
        if not user:
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, ctx.config.snd_secret_key, algorithm=ctx.config.snd_enc_algorithm
        )
        return encoded_jwt

    @router.post(
        "/users/login",
        response_model=Token,
        tags=["users"],
    )
    async def login(
        payload: TokenRequestPayload,
    ) -> dict[str, str]:
        user = await authenticate_user(payload.username, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ctx.config.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @router.post(
        "/users/signup",
        response_model=Token,
        tags=["users"],
    )
    async def signup(
        payload: TokenRequestPayload,
    ) -> dict[str, str]:
        user = await store_user(payload.username, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists or username is taken",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ctx.config.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    return router
