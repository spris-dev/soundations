from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str


class UserInDB(User):
    id: int
    hashed_password: str


class UserTrackSearchPrompt(BaseModel):
    prompt: str = Field(max_length=100)
