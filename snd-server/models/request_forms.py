from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Form


class SignUpRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(),
        password: str = Form(),
        email: str = Form(),
        scope: str = Form(default=""),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
    ) -> None:
        super().__init__(
            grant_type, username, password, scope, client_id, client_secret
        )
        self.email: str = email
