from pydantic import BaseModel
from typing import List
from models.spotify import (
    SpotifyApiTrack,
    SpotifyApiTrackFeaturesResponse,
    SpotifyApiArtist,
)


class SoundationsRawTrack(BaseModel):
    id: str
    popularity: int
    artists: List[SpotifyApiArtist]


class SoundationsRawTrackResponseTracks(BaseModel):
    items: List[SoundationsRawTrack]
    limit: int
    offset: int
    total: int


class SoundationsRawTrackResponse(BaseModel):
    tracks: SoundationsRawTrackResponseTracks


class RecommendedTrack(BaseModel):
    id: str
    similarity: float


class SoundationsTrack(SpotifyApiTrack):
    pass


class SoundationsTrackWithFeatures(
    SoundationsRawTrack, SpotifyApiTrackFeaturesResponse
):
    pass
