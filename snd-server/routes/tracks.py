from fastapi import APIRouter, Query, HTTPException, Response, Depends, status
from result import Ok, Err
from pydantic import BaseModel
from asyncio import gather

from services.track_service import TrackServiceResult
from context import Context
from mappers.soundations import create_track_from_spotify
from models.users import UserInDB
from models.soundations import (
    SoundationsTrack,
    RecommendedTrack,
)


class TracksSearchResponse(BaseModel):
    items: list[SoundationsTrack]
    limit: int
    offset: int
    total: int


class TrackRecommendationsItem(BaseModel):
    track: SoundationsTrack
    recommendation: RecommendedTrack


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
        ctx.tracer.add("track_search_prompt", q)

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
        user: UserInDB | None = Depends(ctx.authorization_service.get_current_user),
        limit: int = Query(default=6, ge=1, le=10),
        offset: int = Query(default=0, ge=0, le=50),
    ) -> TracksRecommendationsResponse:
        if user:
            await ctx.search_history.store_track(user, track_id)

        result = await ctx.track_service.create_track_model_by_id(track_id)

        match result:
            case Ok(track):
                recommendations = await ctx.thread_pool.run_async(
                    ctx.recommender.get_top_n, track, limit
                )

                soundations_tracks: list[
                    TrackServiceResult[SoundationsTrack]
                ] = await gather(
                    *[
                        ctx.track_service.soundations_track_by_id(track.id)
                        for track in recommendations
                    ]
                )

                return TracksRecommendationsResponse(
                    items=[
                        TrackRecommendationsItem(track=t.unwrap(), recommendation=r)
                        for t, r in zip(soundations_tracks, recommendations)
                        if t.is_ok()
                    ],
                    limit=limit,
                    offset=offset,
                    total=len(recommendations),
                )
            case Err(err):
                raise HTTPException(status_code=err.http_code, detail=err.message)

    @router.get(
        "/tracks/personal_recommendations",
        response_model=TracksRecommendationsResponse,
        tags=["tracks"],
    )
    async def get_personal_recommendations(
        prompt: str = Query(min_length=1, max_length=128),
        user: UserInDB | None = Depends(ctx.authorization_service.get_current_user),
        limit: int = Query(default=6, ge=1, le=10),
        offset: int = Query(default=0, ge=0, le=50),
    ) -> TracksRecommendationsResponse:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        recommendations = await ctx.recommender.get_top_n_for_user(prompt, user, limit)

        soundations_tracks: list[TrackServiceResult[SoundationsTrack]] = await gather(
            *[
                ctx.track_service.soundations_track_by_id(track.id)
                for track in recommendations
            ]
        )

        return TracksRecommendationsResponse(
            items=[
                TrackRecommendationsItem(track=t.unwrap(), recommendation=r)
                for t, r in zip(soundations_tracks, recommendations)
                if t.is_ok()
            ],
            limit=limit,
            offset=offset,
            total=len(recommendations),
        )

    return router
