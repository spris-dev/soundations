import httpx
import logging
from fastapi import FastAPI
from fastapi.routing import APIRoute
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from context import Context
from recommendation_engine import Recommender
from services.thread_pool import ThreadPool
from services.track_service import TrackService
from services.search_history import SearchHistory
from services.authorization_service import AuthorizationService
from services.sqlite_storage import SqliteStorage
from services.config import Config
from services.spotify_api import SpotifyApi
from services.tracer import Tracer
from services.users_storage import UsersStorage
from routes.health import create_health_router
from routes.tracks import create_tracks_router
from routes.users import create_users_router


def create_ctx() -> Context:
    ctx = Context()

    ctx.http_client = httpx.AsyncClient()
    ctx.config = Config()
    ctx.spotify_api = SpotifyApi(ctx)
    ctx.sqlite_storage = SqliteStorage(ctx)
    ctx.recommender = Recommender(ctx)
    ctx.thread_pool = ThreadPool()
    ctx.track_service = TrackService(ctx)
    ctx.search_history = SearchHistory(ctx)
    ctx.authorization_service = AuthorizationService(ctx)
    ctx.tracer = Tracer()
    ctx.users_storage = UsersStorage(ctx)

    return ctx


def create_app(ctx: Context) -> FastAPI:
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)

    app.include_router(create_health_router(ctx), prefix="/api")
    app.include_router(create_tracks_router(ctx), prefix="/api")
    app.include_router(create_users_router(ctx), prefix="/api")

    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()

    @app.on_event("startup")
    async def startup():
        configure_logging()
        logger = logging.getLogger()

        if (
            ctx.config.spotify_client_id is not None
            and "dummy" in ctx.config.spotify_client_id
        ):
            logger.info("Using dummy values for Spotify secrets")

        await ctx.sqlite_storage.connect()
        await ctx.sqlite_storage.migrate()

    @app.on_event("shutdown")
    async def shutdown():
        await ctx.sqlite_storage.disconnect()
        await ctx.http_client.aclose()

    return app


def configure_logging(level=logging.INFO):
    """
    @see https://github.com/encode/uvicorn/issues/614#issuecomment-611135458
    """
    logging.getLogger().handlers.clear()

    logging.basicConfig(
        format="%(asctime)s [%(process)d] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S %z]",
        level=level,
    )


def custom_generate_unique_id(route: APIRoute):
    return route.name
