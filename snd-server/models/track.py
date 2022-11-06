from pydantic import BaseModel
from typing import List


class Album(BaseModel):
    id: str
    name: str
    release_date: str
    images: list


class Artist(BaseModel):
    id: str
    name: str


class Track(BaseModel):
    id: str
    name: str
    popularity: int
    release_date: str
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    valence: float
    album: Album
    artists: List[Artist]


class TrackGeneral(BaseModel):
    id: str
    name: str
    popularity: int
    album: Album
    artists: List[Artist]


class TrackFeatures(BaseModel):
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
    type: str
    uri: str
    track_href: str
    analysis_url: str
    duration_ms: int
    time_signature: int
