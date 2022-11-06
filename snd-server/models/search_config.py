from typing import TypedDict
from typing_extensions import NotRequired


class SearchConfig(TypedDict):
    limit: int
    genre: str
    count: int
