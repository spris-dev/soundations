from pydantic import BaseModel


class TokenRequestForm(BaseModel):
    username: str
    password: str
