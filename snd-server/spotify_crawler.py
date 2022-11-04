import requests
import sys
import time
import os
from dotenv import load_dotenv
from services.sounds_storage import SoundsStorage
from models.track import Track, TrackFeatures, TrackGeneral
from result import Ok, Err


audio_features = [
    "id",
    "name",
    "popularity",
    "release_date",
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "key",
    "liveness",
    "loudness",
    "mode",
    "speechiness",
    "tempo",
    "time_signature",
    "valence",
]


class SpotifyCrawler:
    def __init__(self, client_id, client_secret):
        self.sounds_storage = SoundsStorage("dataset.csv")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://accounts.spotify.com/api/token"
        self.token = self.get_access_token()

    def get_access_token(self):
        response = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )

        print("[Response] status_code: " + str(response.status_code), file=sys.stdout)
        print("Access Token Headers: " + str(response.headers), file=sys.stdout)

        return response.json()["access_token"]

    def request(self, url):
        auth = "Bearer " + self.token
        headers = {"Authorization": auth}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(
                "[Response] status_code: " + str(response.status_code), file=sys.stdout
            )
            print("Response headers: " + str(response.headers), file=sys.stdout)

        if response.status_code == 401:
            self.token = self.get_access_token()
            print("Token refreshed")
            self.request(url)

        if response.status_code == 404:
            print("404")
            return Err("Error 404 in request")

        if response.status_code == 429:
            sec_to_sleep = float(response.headers.get("retry-after"))
            time.sleep(sec_to_sleep)
            self.request(url)

        if response.status_code == 503:
            self.request(url)

        return Ok(response.json())

    def search_tracks_by_genre(self, search_config):
        genre = search_config["genre"]
        limit = search_config["limit"]

        url = (
            "https://api.spotify.com/v1/search?q=genre%3A"
            + genre
            + "&type="
            + "track"
            + "&limit="
            + limit
            + "&offset="
        )

        tracks = []
        for i in range(0, 1000, int(limit)):
            curr_url = url + str(i)
            tracks_general = self.request(curr_url)

            if isinstance(tracks_general, Ok):
                for i, t in enumerate(tracks_general.value["tracks"]["items"]):
                    track_features = TrackGeneral.parse_obj(t).dict()

                    extra_features = self.get_track_features(t["id"])
                    if isinstance(extra_features, Ok):
                        track_features.update(extra_features.value.dict())
                        track_features.update(
                            {"release_date": track_features["album"]["release_date"]}
                        )
                        try:
                            new_track = Track.parse_obj(track_features)
                            tracks.append(new_track)
                        except:
                            print("Error while parsing track")

        return tracks

    def get_track_features(self, track_id):
        url = "https://api.spotify.com/v1/audio-features/" + str(track_id)

        try:
            response = TrackFeatures.parse_obj(self.request(url).value)
            return Ok(response)
        except:
            return Err("Failed to parse track features")

    def get_genres_list(self):
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

        response = self.request(url)
        if isinstance(response, Ok):
            return response.value

    def dataset_by_genres(self, genres):
        for genre in genres:
            search_config = {"genre": genre, "limit": str(50)}
            tracks = self.search_tracks_by_genre(search_config)
            self.sounds_storage.store_tracks_csv(tracks)


def main():
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    spotify_crawler = SpotifyCrawler(client_id, client_secret)

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
    ]
    spotify_crawler.dataset_by_genres(your_metal)


if __name__ == "__main__":
    main()
