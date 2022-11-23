from pydantic import BaseModel, Field, conlist, validator
from typing import List


class Album(BaseModel):
    id: str
    name: str
    release_date: str
    images: list


class SpotifyAlbumSearchResponseList(BaseModel):
    albums: List[Album] = Field(alias="items")


class Artist(BaseModel):
    id: str
    name: str


class SpotifyArtistSearchResponseList(BaseModel):
    artists: List[Artist] = Field(alias="artists")

    @validator("artists", pre=True)
    def only_valid_items(cls, v):
        return v["items"]


class SpotifyTrackSearchResponse(BaseModel):
    id: str
    name: str
    popularity: int
    album: Album
    artists: List[Artist]


class SpotifyTrackSearchByAlbumResponseList(BaseModel):
    tracks: List[SpotifyTrackSearchResponse] = Field(alias="items")


class SpotifyTrackSearchResponseList(BaseModel):
    tracks: List[SpotifyTrackSearchResponse] = Field(alias="tracks")

    @validator("tracks", pre=True)
    def only_valid_items(cls, v):
        return v["items"]


class SpotifyTrackFeaturesResponse(BaseModel):
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


class Track(SpotifyTrackSearchResponse, SpotifyTrackFeaturesResponse):
    pass


class TrackList(BaseModel):
    __root__: List[Track]
