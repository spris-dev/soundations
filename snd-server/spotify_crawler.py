import requests
import time

from result import Ok, Err, Result
from typing import TypeVar, List

from services.config import Config
from services.sounds_storage import SoundsStorage
from models.track import (
    Track,
    TrackList,
    SpotifyTrackFeaturesResponse,
    SpotifyTrackSearchResponseList,
)
from models.search_config import SearchConfig


T = TypeVar("T")


class SpotifyCrawler:
    def __init__(self):
        self.config = Config()
        self.spotify_token = ""

        self.token_url = "https://accounts.spotify.com/api/token"
        self.track_by_genre_url = "https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&limit={limit}&offset={offset}"
        self.track_features_url = "https://api.spotify.com/v1/audio-features/{id}"

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

        return Ok(T.parse_obj(response.json()))

    def fetch_tracks_by_genres(self, search_config: SearchConfig) -> List[Track]:
        genre = search_config["genre"]
        count = search_config["count"]
        limit = search_config["limit"]

        tracks = []
        for i in range(0, count, limit):
            url = self.track_by_genre_url.format(genre=genre, limit=limit, offset=i)
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
        self.sounds_storage = SoundsStorage(self.config.sounds_storage_path)

        for genre in genres:
            search_config: SearchConfig = {
                "genre": genre,
                "limit": self.config.spoify_limit,
                "count": self.config.tracks_number_for_genre,
            }

            tracks = self.fetch_tracks_by_genres(search_config)
            self.sounds_storage.store_tracks(tracks)


def main():
    spotify_crawler = SpotifyCrawler()
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
