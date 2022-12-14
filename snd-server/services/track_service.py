from typing import TypeVar
from result import Result, Ok, Err

from services.spotify_api import SpotifyApi, SPOTIFY_API_URL
from context import Context
from models.error import SoundationsError
from models.track import Track, SpotifyTrackSearchResponse, SpotifyTrackFeaturesResponse
from models.soundations import SoundationsTrack


TOk = TypeVar("TOk")
TrackServiceResult = Result[TOk, SoundationsError]


class TrackService:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.api = SpotifyApi(ctx)

    async def create_track_model_by_id(self, id: str) -> TrackServiceResult[Track]:
        track_search_url = f"{SPOTIFY_API_URL}/tracks/{id}"
        track_features_url = f"{SPOTIFY_API_URL}/audio-features/{id}"

        track_search_result = await self.api.call_spotify_api(
            lambda headers: self.ctx.http_client.get(
                url=track_search_url,
                headers=headers,
            ),
            model=SpotifyTrackSearchResponse,
        )

        track_features_result = await self.api.call_spotify_api(
            lambda headers: self.ctx.http_client.get(
                url=track_features_url,
                headers=headers,
            ),
            model=SpotifyTrackFeaturesResponse,
        )

        if isinstance(track_search_result, Ok) and isinstance(
            track_features_result, Ok
        ):
            track_search_result = track_search_result.value
            track_features_result = track_features_result.value

            track = Track(
                id=track_search_result.id,
                name=track_search_result.name,
                popularity=track_search_result.popularity,
                album=track_search_result.album,
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
        track_search_url = f"{SPOTIFY_API_URL}/tracks/{id}"

        track_search_result = await self.api.call_spotify_api(
            lambda headers: self.ctx.http_client.get(
                url=track_search_url,
                headers=headers,
            ),
            model=SoundationsTrack,
        )

        if isinstance(track_search_result, Ok):
            track_search_result = track_search_result.value

            soundations_track = SoundationsTrack(
                id=track_search_result.id,
                name=track_search_result.name,
                album=track_search_result.album,
                artists=track_search_result.artists,
                duration_ms=track_search_result.duration_ms,
                href=track_search_result.href,
                preview_url=track_search_result.preview_url,
            )

            return Ok(soundations_track)

        return Err(SoundationsError(424, "Somethings bad happened on Spotify side"))
