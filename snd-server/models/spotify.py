from pydantic import BaseModel
from typing import List, Optional


class SpotifyApiImage(BaseModel):
    height: int
    width: int
    url: str


class SpotifyApiAlbum(BaseModel):
    id: str
    name: str
    release_date: str
    images: List[SpotifyApiImage]


class SpotifyApiArtist(BaseModel):
    id: str
    name: str


class SpotifyApiTrack(BaseModel):
    id: str
    name: str
    album: SpotifyApiAlbum
    artists: List[SpotifyApiArtist]
    popularity: int
    duration_ms: int
    href: str
    preview_url: Optional[str] = None


class SpotifyApiTrackFeaturesResponse(BaseModel):
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int


class SpotifyApiTrackSearchResponseTracks(BaseModel):
    items: List[SpotifyApiTrack]
    limit: int
    offset: int
    total: int


class SpotifyApiTrackSearchResponse(BaseModel):
    tracks: SpotifyApiTrackSearchResponseTracks


class SpotifyApiError(BaseModel):
    status: int
    message: str


class SpotifyApiErrorResponse(BaseModel):
    error: SpotifyApiError
