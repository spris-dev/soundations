from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient
    from services.sqlite_storage import SqliteStorage
    from services.config import Config
    from services.spotify_api import SpotifyApi
    from services.thread_pool import ThreadPool
    from services.track_service import TrackService
    from services.tracer import Tracer
    from recommendation_engine import Recommender


class Context:
    sqlite_storage: "SqliteStorage"
    config: "Config"
    http_client: "AsyncClient"
    spotify_api: "SpotifyApi"
    recommender: "Recommender"
    track_service: "TrackService"
    thread_pool: "ThreadPool"
    tracer: "Tracer"
