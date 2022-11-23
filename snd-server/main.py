import datetime
from fastapi import FastAPI

from context import Context
from services.sqlite_storage import SqliteStorage
from services.config import Config
from routes.health import create_health_router

app = FastAPI()
ctx = Context()


@app.on_event("startup")
async def startup():
    ctx.config = Config()

    if (
        ctx.config.spotify_client_id is not None
        and "dummy" in ctx.config.spotify_client_id
    ):
        print("[Config]: Using dummy values for Spotify secrets")

    ctx.sqlite_storage = SqliteStorage(ctx)
    await ctx.sqlite_storage.connect()
    await ctx.sqlite_storage.migrate()

    app.include_router(create_health_router(ctx), prefix="/api")


@app.on_event("shutdown")
async def shutdown():
    await ctx.sqlite_storage.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World", "now": format(datetime.datetime.now())}
