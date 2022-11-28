import argparse
import requests
import time

from result import Ok, Err, Result
from typing import TypeVar, List

from services.config import Config
from services.sounds_storage import SoundsStorage
from models.track import (
    Track,
    Artist,
    Album,
    SpotifyAlbumSearchResponseList,
    SpotifyArtistSearchResponseList,
    SpotifyAlbumSearchResponseList,
    SpotifyArtistSearchResponseList,
    SpotifyTrackFeaturesResponse,
    SpotifyTrackSearchResponseList,
)


T = TypeVar("T")


class SpotifyCrawler:
    def __init__(self, resume: bool):
        self.resume = resume
        self.config = Config()
        self.spotify_token = ""

        self.token_url = "https://accounts.spotify.com/api/token"
        self.track_by_genre_url = "https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&limit={limit}&offset={offset}"
        self.artist_by_genre_url = "https://api.spotify.com/v1/search?q=genre%3A{genre}&type=artist&limit={limit}&offset={offset}"
        self.track_features_url = "https://api.spotify.com/v1/audio-features/{id}"
        self.artists_album_url = "https://api.spotify.com/v1/artists/{id}/albums?q=include_groups=album&limit={limit}&offset={offset}"
        self.artists_tracks_url = "https://api.spotify.com/v1/search?q=artist%3A'{name}'&type=track&limit={limit}&offset={offset}"

        self.artists_ids = set()

    def set_access_token(self):
        response = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(self.config.spotify_client_id, self.config.spotify_client_secret),
        )

        print("[Response] status_code: " + str(response.status_code))
        print("Access Token Headers: " + str(response.headers))

        self.spotify_token = response.json()["access_token"]

    def request(self, url, T) -> Result[T, str]:
        auth = "Bearer " + self.spotify_token
        headers = {"Authorization": auth}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("[Response] status_code: " + str(response.status_code))
            print("Response headers: " + str(response.headers))

            if response.status_code == 401:
                self.set_access_token()
                print("Token refreshed")
                return self.request(url, T)

            if response.status_code == 404:
                print("404")
                return Err("Error 404 in request")

            if response.status_code == 429:
                sec_to_sleep = response.headers.get("retry-after")
                if sec_to_sleep is not None:
                    time.sleep(float(sec_to_sleep))
                    return self.request(url, T)

            if response.status_code == 503:
                return self.request(url, T)

            return Err("Unknown error in request")

        try:
            return Ok(T.parse_obj(response.json()))
        except:
            return Err("Error while parsing in request")

    def fetch_artists_by_genre(self, genre: str) -> List[Artist]:
        artists = []
        for i in range(0, self.config.items_per_search, self.config.spotify_limit):
            url = self.artist_by_genre_url.format(
                genre=genre, limit=self.config.spotify_limit, offset=i
            )
            artists_response = self.request(url, SpotifyArtistSearchResponseList)
            if isinstance(artists_response, Ok):
                artists.extend(artists_response.value.artists)

        return artists

    def fetch_artist_tracks(self, artist: Artist) -> List[Track]:
        tracks = []
        for i in range(0, self.config.items_per_search, self.config.spotify_limit):
            url = self.artists_tracks_url.format(
                name=artist.name, limit=self.config.spotify_limit, offset=i
            )
            tracks_general = self.request(url, SpotifyTrackSearchResponseList)

            if isinstance(tracks_general, Ok):
                tracks_general = tracks_general.value.tracks
                for track in tracks_general:
                    correct_artist = False
                    for a in track.artists:
                        if artist.id == a.id:
                            correct_artist = True

                    if not correct_artist:
                        continue

                    extra_features = self.fetch_track_features(track.id)

                    if isinstance(extra_features, Ok):
                        try:
                            track = track.dict()
                            track.update(extra_features.value.dict())
                            tracks.append(Track.parse_obj(track))
                        except:
                            print("Error while parsing track")

        return tracks

    def fetch_albums_by_artist(self, artist: Artist) -> Result[List[Album], str]:
        artist_id = artist.id

        url = self.artists_album_url.format(id=artist_id, limit=10, offset=0)
        albums = self.request(url, SpotifyAlbumSearchResponseList)

        if isinstance(albums, Ok):
            return Ok(albums.value.albums)
        else:
            return Err("Error while parsing album")

    def fetch_tracks_by_genre(self, genre: str) -> List[Track]:
        tracks = []
        for i in range(0, self.config.items_per_search, self.config.spotify_limit):
            url = self.track_by_genre_url.format(
                genre=genre, limit=self.config.spotify_limit, offset=i
            )
            tracks_general = self.request(url, SpotifyTrackSearchResponseList)

            if isinstance(tracks_general, Ok):
                tracks_general = tracks_general.value.tracks
                for track in tracks_general:
                    extra_features = self.fetch_track_features(track.id)

                    if isinstance(extra_features, Ok):
                        try:
                            track = track.dict()
                            track.update(extra_features.value.dict())
                            tracks.append(Track.parse_obj(track))
                        except:
                            print("Error while parsing track")

        return tracks

    def fetch_track_features(
        self, track_id
    ) -> Result[SpotifyTrackFeaturesResponse, str]:
        url = self.track_features_url

        try:
            response = SpotifyTrackFeaturesResponse.parse_obj(
                self.request(
                    url.format(id=track_id), SpotifyTrackFeaturesResponse
                ).value
            )
            return Ok(response)
        except:
            return Err("Failed to parse track features")

    def store_dataset_by_genres(self, genres):
        self.sounds_storage = SoundsStorage()
        if self.resume:
            self.artists_ids = self.sounds_storage.get_artists()
            print(self.artists_ids)
        else:
            self.sounds_storage.write_headers()

        for genre in genres:
            print(genre)
            artists = self.fetch_artists_by_genre(genre)
            print(artists)

            for artist in artists:
                print(artist)
                if artist.id in self.artists_ids:
                    print("True")
                    continue

                tracks = self.fetch_artist_tracks(artist)
                print(len(tracks))

                self.artists_ids.add(artist.id)
                self.sounds_storage.store_tracks(tracks)
                self.sounds_storage.store_artist(artist.id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--resume",
        action="store_true",
        help="start crawling from the point where you stopped",
    )
    args = parser.parse_args()

    spotify_crawler = SpotifyCrawler(args.resume)
    spotify_crawler.set_access_token()

    your_metal = [
        "alt-rock",
        "alternative",
        "black-metal",
        "death-metal",
        "emo",
        "grunge",
        "hard-rock",
        "hardcore",
        "heavy-metal",
        "j-rock",
        "metal",
        "metal-misc",
        "metalcore",
        "psych-rock",
        "punk",
        "punk-rock",
        "rock",
        "rock-n-roll",
        "rockabilly",
        "classical",
        "hip-hop",
        "indie-pop",
        "drum-and-bass",
        "indie-pop",
    ]

    spotify_crawler.store_dataset_by_genres(your_metal)


if __name__ == "__main__":
    main()
