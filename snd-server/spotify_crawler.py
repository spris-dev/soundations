import asyncio

from fastapi import HTTPException
from result import Ok, Err
from typing import TypeVar, List

from context import Context
from services.sounds_storage import SoundsStorage

from models.spotify import (
    SpotifyApiArtist,
    SpotifyApiTrackFeaturesResponse,
)

from models.soundations import SoundationsTrackWithFeatures


T = TypeVar("T")


def crawl_tracks_by_genres(ctx: Context, resume: bool, genres) -> None:
    spotify_crawler = SpotifyCrawler(ctx, resume)

    spotify_crawler.fetch_tracks_by_genres(genres)


class SpotifyCrawler:
    def __init__(self, ctx: Context, resume: bool) -> None:
        self.ctx = ctx
        self.resume = resume

        self.sounds_storage = SoundsStorage(ctx)
        self.artists_ids = set()

    async def __fetch_artists_by_genre(self, genre: str) -> List[SpotifyApiArtist]:
        spotify_artists: list[SpotifyApiArtist] = []
        for i in range(
            0, self.ctx.config.items_per_search, self.ctx.config.spotify_limit
        ):
            artists_search_result = await self.ctx.spotify_api.search_artists_by_genre(
                genre, self.ctx.config.spotify_limit, i
            )

            match artists_search_result:
                case Ok(result):
                    spotify_artists.extend(result.artists.items)

                case Err(err):
                    raise HTTPException(status_code=err.http_code, detail=err.message)

        return spotify_artists

    async def __fetch_track_features(self, track_id) -> SpotifyApiTrackFeaturesResponse:
        track_features_result = await self.ctx.spotify_api.get_track_features(
            track_id=track_id
        )

        match track_features_result:
            case Ok(result):
                return result

            case Err(err):
                raise HTTPException(status_code=err.http_code, detail=err.message)

    async def __fetch_artist_tracks(
        self, artist: SpotifyApiArtist
    ) -> List[SoundationsTrackWithFeatures]:
        tracks: list[SoundationsTrackWithFeatures] = []
        for i in range(
            0, self.ctx.config.items_per_search, self.ctx.config.spotify_limit
        ):
            tracks_search_result = await self.ctx.spotify_api.search_tracks_by_artist(
                artist=artist, limit=self.ctx.config.spotify_limit, offset=i
            )

            match tracks_search_result:
                case Ok(result):
                    for raw_track in result.items:
                        track_with_features = await self.__fetch_track_features(
                            raw_track.id
                        )

                        track = SoundationsTrackWithFeatures(
                            id=raw_track.id,
                            popularity=raw_track.popularity,
                            artists=raw_track.artists,
                            danceability=track_with_features.danceability,
                            energy=track_with_features.energy,
                            key=track_with_features.key,
                            loudness=track_with_features.loudness,
                            mode=track_with_features.mode,
                            speechiness=track_with_features.speechiness,
                            acousticness=track_with_features.acousticness,
                            instrumentalness=track_with_features.instrumentalness,
                            liveness=track_with_features.liveness,
                            valence=track_with_features.valence,
                            tempo=track_with_features.tempo,
                            duration_ms=track_with_features.duration_ms,
                            time_signature=track_with_features.time_signature,
                        )

                        tracks.append(track)

                case Err(err):
                    raise HTTPException(status_code=err.http_code, detail=err.message)

        return tracks

    async def __fetch_tracks_by_genre(self, genres) -> None:
        for genre in genres:
            artists = await self.__fetch_artists_by_genre(genre)

            for artist in artists:
                if artist.id in self.artists_ids:
                    continue

                tracks = await self.__fetch_artist_tracks(artist)
                self.artists_ids.add(artist.id)

                self.sounds_storage.store_tracks(tracks)
                self.sounds_storage.store_artist(artist.id)

    def fetch_tracks_by_genres(self, genres) -> None:
        if self.resume:
            self.artists_ids = self.sounds_storage.get_artists()
        else:
            self.sounds_storage.write_headers()

        asyncio.run(self.__fetch_tracks_by_genre(genres))
