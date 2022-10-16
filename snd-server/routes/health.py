from fastapi import APIRouter

from context import Context


def create_health_router(ctx: Context):
    router = APIRouter()

    @router.get("/health")
    async def health():
        return {
            "ok": True,
        }

    return router
