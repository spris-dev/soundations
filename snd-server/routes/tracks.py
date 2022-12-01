from fastapi import APIRouter, Query, HTTPException, Response
from result import Ok, Err
from pydantic import BaseModel

from context import Context
from models.soundations import SoundationsTrack
from mappers.soundations import create_track_from_spotify


class TracksSearchResponse(BaseModel):
    items: list[SoundationsTrack]
    limit: int
    offset: int
    total: int


class TrackRecommendationsItem(SoundationsTrack):
    score: float


class TracksRecommendationsResponse(BaseModel):
    items: list[TrackRecommendationsItem]
    limit: int
    offset: int
    total: int


def create_tracks_router(ctx: Context):
    router = APIRouter()

    @router.get("/tracks", response_model=TracksSearchResponse, tags=["tracks"])
    async def get_tracks(
        response: Response,
        q: str = Query(min_length=1, max_length=128),
        limit: int = Query(default=5, ge=1, le=10),
        offset: int = Query(default=0, ge=0, le=1000),
    ) -> TracksSearchResponse:
        result = await ctx.spotify_api.search_tracks(q=q, limit=limit, offset=offset)

        match result:
            case Ok(tracks):
                response.headers["Cache-Control"] = "public, max-age=7200"

                return TracksSearchResponse(
                    items=[create_track_from_spotify(item) for item in tracks.items],
                    limit=tracks.limit,
                    offset=tracks.offset,
                    total=tracks.total,
                )
            case Err(err):
                raise HTTPException(status_code=err.http_code, detail=err.message)

    @router.get(
        "/tracks/{track_id}/recommendations",
        response_model=TracksRecommendationsResponse,
        tags=["tracks"],
    )
    async def get_track_recommendations(
        track_id: str,
        limit: int = Query(default=6, ge=1, le=10),
        offset: int = Query(default=0, ge=0, le=50),
    ) -> TracksRecommendationsResponse:
        # TODO: add actual recommendations impl

        return TracksRecommendationsResponse(
            items=[],
            limit=limit,
            offset=offset,
            total=0,
        )

    return router