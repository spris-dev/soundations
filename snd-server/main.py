import datetime
import httpx
import logging
from fastapi import FastAPI

from context import Context
from services.sqlite_storage import SqliteStorage
from services.config import Config
from services.spotify_api import SpotifyApi
from routes.health import create_health_router

app = FastAPI()
ctx = Context()


@app.on_event("startup")
async def startup():
    configure_logging()
    logger = logging.getLogger()

    ctx.http_client = httpx.AsyncClient()
    ctx.config = Config()
    ctx.spotify_api = SpotifyApi(ctx)

    if (
        ctx.config.spotify_client_id is not None
        and "dummy" in ctx.config.spotify_client_id
    ):
        logger.info("Using dummy values for Spotify secrets")

    ctx.sqlite_storage = SqliteStorage(ctx)
    await ctx.sqlite_storage.connect()
    await ctx.sqlite_storage.migrate()

    app.include_router(create_health_router(ctx), prefix="/api")


@app.on_event("shutdown")
async def shutdown():
    await ctx.sqlite_storage.disconnect()
    await ctx.http_client.aclose()


@app.get("/")
async def root():
    return {"message": "Hello World", "now": format(datetime.datetime.now())}


def configure_logging(level=logging.INFO):
    """
    @see https://github.com/encode/uvicorn/issues/614#issuecomment-611135458
    """
    logging.getLogger().handlers.clear()

    logging.basicConfig(
        format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S %z]",
        level=level,
    )
