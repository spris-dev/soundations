from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient
    from services.sqlite_storage import SqliteStorage
    from services.config import Config
    from services.spotify_api import SpotifyApi


class Context:
    sqlite_storage: "SqliteStorage"
    config: "Config"
    http_client: "AsyncClient"
    spotify_api: "SpotifyApi"
