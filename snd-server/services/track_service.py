from fastapi import HTTPException
from typing import TypeVar
from result import Result, Ok, Err

from services.spotify_api import SpotifyApi
from context import Context
from models.error import SoundationsError
from models.soundations import (
    SoundationsTrack,
    SoundationsTrackWithFeatures,
)


TOk = TypeVar("TOk")
TrackServiceResult = Result[TOk, SoundationsError]


class TrackService:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.api = SpotifyApi(ctx)

    async def create_track_model_by_id(
        self, id: str
    ) -> TrackServiceResult[SoundationsTrackWithFeatures]:
        track_search_result = await self.api.get_track(id)
        track_features_result = await self.api.get_track_features(id)

        if isinstance(track_search_result, Ok) and isinstance(
            track_features_result, Ok
        ):
            track_search_result = track_search_result.value
            track_features_result = track_features_result.value

            track = SoundationsTrackWithFeatures(
                id=track_search_result.id,
                popularity=track_search_result.popularity,
                artists=track_search_result.artists,
                danceability=track_features_result.danceability,
                energy=track_features_result.energy,
                key=track_features_result.key,
                loudness=track_features_result.loudness,
                mode=track_features_result.mode,
                speechiness=track_features_result.speechiness,
                acousticness=track_features_result.acousticness,
                instrumentalness=track_features_result.instrumentalness,
                liveness=track_features_result.liveness,
                valence=track_features_result.valence,
                tempo=track_features_result.tempo,
                duration_ms=track_features_result.duration_ms,
                time_signature=track_features_result.time_signature,
            )

            return Ok(track)

        return Err(SoundationsError(424, "Somethings bad happened on Spotify side"))

    async def soundations_track_by_id(
        self, id: str
    ) -> TrackServiceResult[SoundationsTrack]:
        track_search_result = await self.api.get_track(id)

        match track_search_result:
            case Ok(result):
                soundations_track = SoundationsTrack(
                    id=result.id,
                    name=result.name,
                    popularity=result.popularity,
                    album=result.album,
                    artists=result.artists,
                    duration_ms=result.duration_ms,
                    href=result.href,
                    preview_url=result.preview_url,
                )
                return Ok(soundations_track)

            case Err(err):
                raise HTTPException(status_code=err.http_code, detail=err.message)
            case Err(err):
                raise HTTPException(status_code=err.http_code, detail=err.message)
