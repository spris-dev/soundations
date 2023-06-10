import asyncio
import random

from result import Ok, Err, Result
from typing import TypeVar, List

from fastapi import HTTPException
from context import Context
from services.sounds_storage import SoundsStorage
from models.error import SoundationsError

from models.spotify import (
    SpotifyApiArtist,
    SpotifyApiTrackFeaturesResponse,
)

from models.soundations import SoundationsTrackWithFeatures


T = TypeVar("T")


def crawl_tracks_by_genres(ctx: Context, resume: bool, genres) -> None:
    spotify_crawler = SpotifyCrawler(ctx, resume)

    spotify_crawler.fetch_tracks_by_genres(genres)


async def get_tracks_by_genre(
    ctx: Context, genre: str, limit: int = 1, offset: int = 0
) -> List[SoundationsTrackWithFeatures]:
    spotify_crawler = SpotifyCrawler(ctx, resume=False)

    return await spotify_crawler.find_tracks_by_genre(genre, limit, offset)


class SpotifyCrawler:
    def __init__(self, ctx: Context, resume: bool) -> None:
        self.ctx = ctx
        self.resume = resume

        self.sounds_storage = SoundsStorage(ctx)
        self.artists_ids = set()

    async def __fetch_artists_by_genre(
        self, genre: str
    ) -> Result[List[SpotifyApiArtist], SoundationsError]:
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
                    return Err(
                        SoundationsError(
                            404, f"Failed to fetch artists from Spotify: {str(err)}"
                        )
                    )

        return Ok(spotify_artists)

    async def __fetch_track_features(
        self, track_id
    ) -> Result[SpotifyApiTrackFeaturesResponse, SoundationsError]:
        track_features_result = await self.ctx.spotify_api.get_track_features(
            track_id=track_id
        )

        match track_features_result:
            case Ok(result):
                return Ok(result)

            case Err(err):
                return Err(
                    SoundationsError(
                        404, f"Failed to fetch features from Spotify: {str(err)}"
                    )
                )

    async def __fetch_artist_tracks(
        self, artist: SpotifyApiArtist
    ) -> Result[List[SoundationsTrackWithFeatures], SoundationsError]:
        tracks: list[SoundationsTrackWithFeatures] = []
        for i in range(
            0, self.ctx.config.items_per_search, self.ctx.config.spotify_limit
        ):
            tracks_search_result = await self.ctx.spotify_api.search_tracks_by_artist(
                artist=artist, limit=self.ctx.config.spotify_limit, offset=i
            )

            match tracks_search_result:
                case Ok(result):
                    for track in result.items:
                        features_result = await self.__fetch_track_features(track.id)
                        match features_result:
                            case Ok(features):
                                track_with_features = SoundationsTrackWithFeatures(
                                    id=track.id,
                                    popularity=track.popularity,
                                    artists=track.artists,
                                    danceability=features.danceability,
                                    energy=features.energy,
                                    key=features.key,
                                    loudness=features.loudness,
                                    mode=features.mode,
                                    speechiness=features.speechiness,
                                    acousticness=features.acousticness,
                                    instrumentalness=features.instrumentalness,
                                    liveness=features.liveness,
                                    valence=features.valence,
                                    tempo=features.tempo,
                                    duration_ms=features.duration_ms,
                                    time_signature=features.time_signature,
                                )

                                tracks.append(track_with_features)

                            case Err():
                                continue

                case Err(err):
                    return Err(
                        SoundationsError(
                            404, f"Failed to fetch tracks from Spotify: {str(err)}"
                        )
                    )

        return Ok(tracks)

    async def __fetch_tracks_by_genre(self, genres) -> None:
        for genre in genres:
            artists_fetch_result = await self.__fetch_artists_by_genre(genre)
            match artists_fetch_result:
                case Ok(artists):
                    for artist in artists:
                        if artist.id in self.artists_ids:
                            continue

                        tracks_fetch_result = await self.__fetch_artist_tracks(artist)
                        match tracks_fetch_result:
                            case Ok(tracks):
                                self.artists_ids.add(artist.id)

                                self.sounds_storage.store_tracks(tracks)
                                self.sounds_storage.store_artist(artist.id)
                            case Err():
                                continue

                case Err():
                    continue

    async def __fetch_random_artists_by_genre(
        self, genre, limit: int = 1
    ) -> Result[list[SpotifyApiArtist], SoundationsError]:
        artists_search_result = await self.ctx.spotify_api.search_artists_by_genre(
            genre,
            limit,
            random.randint(
                0, self.ctx.config.artists_by_genre_max_spotify_offset - limit
            ),
        )

        spotify_artists = []
        match artists_search_result:
            case Ok(result):
                spotify_artists.extend(result.artists.items)

            case Err(err):
                return Err(
                    SoundationsError(
                        404, f"Failed to fetch artists from Spotify: {str(err)}"
                    )
                )

        return Ok(spotify_artists)

    async def find_tracks_by_genre(
        self, genre: str, limit: int = 1, offset: int = 0
    ) -> List[SoundationsTrackWithFeatures]:
        spotify_artists = await self.__fetch_random_artists_by_genre(
            genre, self.ctx.config.artists_by_genre_limit
        )

        tracks = []
        match spotify_artists:
            case Ok(artists):
                for artist in artists:
                    tracks_search_result = (
                        await self.ctx.spotify_api.search_tracks_by_artist(
                            artist=artist,
                            limit=self.ctx.config.tracks_by_artist_limit,
                            offset=offset,
                        )
                    )
                    match tracks_search_result:
                        case Ok(result):
                            for track in result.items:
                                features_result = await self.__fetch_track_features(
                                    track.id
                                )
                                match features_result:
                                    case Ok(features):
                                        track_with_features = SoundationsTrackWithFeatures(
                                            id=track.id,
                                            popularity=track.popularity,
                                            artists=track.artists,
                                            danceability=features.danceability,
                                            energy=features.energy,
                                            key=features.key,
                                            loudness=features.loudness,
                                            mode=features.mode,
                                            speechiness=features.speechiness,
                                            acousticness=features.acousticness,
                                            instrumentalness=features.instrumentalness,
                                            liveness=features.liveness,
                                            valence=features.valence,
                                            tempo=features.tempo,
                                            duration_ms=features.duration_ms,
                                            time_signature=features.time_signature,
                                        )

                                        tracks.append(track_with_features)

                                    case Err():
                                        continue

                        case Err(err):
                            continue
            case Err(err):
                raise HTTPException(status_code=err.http_code, detail=err.message)
        return tracks

    def fetch_tracks_by_genres(self, genres) -> None:
        if self.resume:
            self.artists_ids = self.sounds_storage.get_artists()
        else:
            self.sounds_storage.write_headers()

        asyncio.run(self.__fetch_tracks_by_genre(genres))
