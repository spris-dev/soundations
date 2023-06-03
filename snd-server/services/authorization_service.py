from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated

from context import Context
from models.users import TokenData, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


class AuthorizationService:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ) -> UserInDB | None:
        if token is None:
            return None
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.ctx.config.snd_secret_key,
                algorithms=self.ctx.config.snd_enc_algorithm,
            )
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.ctx.users_storage.get_user(username=str(username))
        if user is None:
            raise credentials_exception
        return user
