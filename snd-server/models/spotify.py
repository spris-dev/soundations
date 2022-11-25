from pydantic import BaseModel
from typing import List


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
    duration_ms: int
    href: str
    preview_url: str


class SpotifyApiTrackSearchResponseTracks(BaseModel):
    items: List[SpotifyApiTrack]


class SpotifyApiTrackSearchResponse(BaseModel):
    tracks: SpotifyApiTrackSearchResponseTracks
