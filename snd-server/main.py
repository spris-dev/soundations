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
    ctx.sqlite_storage = SqliteStorage(ctx)

    app.include_router(create_health_router(ctx), prefix="/api")

@app.on_event("shutdown")
async def shutdown():
    ctx.sqlite_storage.connection.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}
