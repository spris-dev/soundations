from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient
    from services.sqlite_storage import SqliteStorage
    from services.config import Config
    from services.spotify_api import SpotifyApi
    from services.thread_pool import ThreadPool
    from services.track_service import TrackService
    from services.search_history import SearchHistory
    from services.users_storage import UsersStorage
    from services.authorization_service import AuthorizationService
    from services.tracer import Tracer
    from recommendation_engine import Recommender


class Context:
    sqlite_storage: "SqliteStorage"
    config: "Config"
    http_client: "AsyncClient"
    spotify_api: "SpotifyApi"
    recommender: "Recommender"
    track_service: "TrackService"
    authorization_service: "AuthorizationService"
    thread_pool: "ThreadPool"
    tracer: "Tracer"
    users_storage: "UsersStorage"
    search_history: "SearchHistory"
