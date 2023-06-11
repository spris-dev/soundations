DEFAULT_MESSAGE = (
    "Something went terribly wrong. Hopefully we're looking at the logs already."
)


class SoundationsError:
    http_code: int
    message: str

    def __init__(self, http_code: int = 400, message: str | None = DEFAULT_MESSAGE):
        self.http_code = http_code
        self.message = message or DEFAULT_MESSAGE

    def __repr__(self):
        return f"{self.http_code} - {self.message}"
